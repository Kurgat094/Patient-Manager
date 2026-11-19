
from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

from .services.auth_services import signup_user, login_user
from .services.patient_service import get_patients,register_patient,view_patient,add_vital,add_visit,get_visits_by_date
from django.urls import reverse
from django.contrib import messages



def register(request):
    if request.session.get("access_token"):
        return redirect('')
    
    print (" we are reaching herr")
    
    if request.method == "POST":
        firstname = request.POST.get("first_name","").strip()
        lastname = request.POST.get("last_name","").strip()
        email = request.POST.get("email","").strip().lower()
        password = request.POST.get("password","")
        confirm_password = request.POST.get("confirm_password","")
        
        values = {
            "first_name": firstname,
            "last_name": lastname,
            "email": email,
        }
        
        errors = {}
        
    
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if len(password) < 6:
            errors["password"] = "Password must contain at least 6 characters."

        if errors:
            return render(request, "auth/register.html", {
                "errors": errors,
                "values": values,
            })

        payload = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password,
        }
        
        status, data = signup_user(payload)
        
        if status == 200 and data.get("success") is True:
            return render(request, "auth/login.html", {
                "success": data.get(
                    "message",
                    "Account created successfully. Please sign in."
                ),
                "email": email,
            })

   

        return render(request, "auth/register.html", {
            "error": data.get(
                "message",
                "Registration failed. Please try again."
            ),
            "errors": data.get("errors", {}),
            "values": values,
        })
        
    return render(request,'auth/register.html')


def login(request):
    if request.session.get("access_token"):
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not email or not password:
            return render(request, "auth/login.html", {
                "error": "Please enter your email and password.",
                "email": email,
            })

        payload = {
            "email": email,
            "password": password,
        }

        status, data = login_user(payload)

        if (
            status == 200
            and data.get("success") is True
            and data.get("data", {}).get("access_token")
        ):
            user_data = data["data"]

            request.session.cycle_key()

            request.session["access_token"] = user_data["access_token"]

            request.session["auth_user"] = {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
            }

            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("dashboard")

        return render(request, "auth/login.html", {
            "error": data.get(
                "message",
                "Invalid email or password."
            ),
            "email": email,
        })

    return render(request, "auth/login.html", {
        "next": request.GET.get("next", ""),
    })

def logout_view(request):
    request.session.flush()

    messages.success(request, "You have successfully logged out.")

    return redirect("login")

def dashboard(request):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return redirect("login")

    print("acess " ,access_token)

    patients = get_patients(access_token)

    context = {
        "auth_user": auth_user,
        "patients": patients,
        "total_patients": len(patients),
    }

    return render(request, "index.html", context)


def getpatients(request):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return redirect("login")

    patients = get_patients(access_token)
    


    context = {
        "auth_user": auth_user,
        "patients": patients,
        "total_patients": len(patients),
    }
    
    return render(request, "patient-list.html",context)


def patient_add(request):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return redirect("login")

    if request.method != "POST":
        return redirect("getpatients")

    payload = {
        "firstname": request.POST.get("firstname", "").strip(),
        "lastname": request.POST.get("lastname", "").strip(),
        "unique": request.POST.get("unique", "").strip(),
        "dob": request.POST.get("dob", "").strip(),
        "gender": request.POST.get("gender", "").strip(),
        "reg_date": request.POST.get("reg_date", "").strip(),
    }

    if not all(payload.values()):
        messages.error(request, "Please complete all patient fields.")
        return redirect("getpatients")

    success, response_data = register_patient(
        access_token,
        payload,
        acc=request.POST.get("acc") or None
    )

    print("REGISTRATION RESULT:", success)
    print("REGISTRATION DATA:", response_data)

    if success:
        messages.success(
            request,
            response_data.get("message", "Patient registered successfully.")
        )
    else:
        messages.error(
            request,
            response_data.get(
                "message",
                "Patient registration failed."
            )
        )

    return redirect("getpatients")

def viewpatient(request, id):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return redirect("login")

    # Retrieve the selected patient from the API
    patient = view_patient(access_token, id)

    if not patient:
        messages.error(request, "Patient details could not be retrieved.")
        return redirect("getpatients")

    context = {
        "auth_user": auth_user,
        "patient": patient,
    }

    return render(request, "view-patient.html", context)




def add_vitals(request, patient_id):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "message": "Your session has expired. Please log in again.",
                "redirect": "/login/",
            }, status=401)

        return redirect("login")

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    visit_date = request.POST.get("visit_date", "").strip()
    height = request.POST.get("height", "").strip()
    weight = request.POST.get("weight", "").strip()

    if not all([visit_date, height, weight]):
        return JsonResponse({
            "success": False,
            "message": "All vitals fields are required."
        }, status=400)

    try:
        height_cm = Decimal(height)
        weight_kg = Decimal(weight)

        if not height_cm.is_finite() or not weight_kg.is_finite():
            raise ValueError("Invalid measurement.")

        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError("Measurements must be positive.")

        height_m = height_cm / Decimal("100")

        bmi = (
            weight_kg / (height_m * height_m)
        ).quantize(Decimal("0.01"))

        # Validate date
        date.fromisoformat(visit_date)

    except (InvalidOperation, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Please enter valid measurements and visit date."
        }, status=400)

    payload = {
        "visit_date": visit_date,
        "height": str(height_cm),
        "weight": str(weight_kg),
        "bmi": str(bmi),
        "patient_id": str(patient_id),
    }

    success, response_data = add_vital(
        access_token,
        payload
    )

    if not success:
        return JsonResponse({
            "success": False,
            "message": response_data.get(
                "message",
                "Unable to save patient vitals."
            )
        }, status=400)

    vital_data = response_data.get("data", {})
    vital_id = vital_data.get("id")

    if not vital_id:
        return JsonResponse({
            "success": False,
            "message": "Vitals were saved, but the API did not return a vital ID."
        }, status=502)

    assessment_type = (
        "general" if bmi <= Decimal("25") else "overweight"
    )

    request.session["pending_assessment"] = {
        "patient_id": patient_id,
        "vital_id": vital_id,
        "bmi": float(bmi),
        "visit_date": visit_date,
        "assessment_type": assessment_type,
    }

    return JsonResponse({
        "success": True,
        "message": f"Vitals saved successfully. BMI: {bmi}",
        "bmi": float(bmi),
        "vital_id": vital_id,
        "assessment_type": assessment_type,
    })
    
    
    
def add_assessment(request, patient_id):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return JsonResponse({
            "success": False,
            "message": "Your session has expired. Please log in again.",
            "redirect": "/login/",
        }, status=401)

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=405)

    
    pending = request.session.get("pending_assessment")

    if (
        not pending
        or str(pending.get("patient_id")) != str(patient_id)
        or not pending.get("vital_id")
    ):
        return JsonResponse({
            "success": False,
            "message": "Please record patient vitals before submitting an assessment."
        }, status=400)

    assessment_type = pending.get("assessment_type")

    general_health = request.POST.get(
        "general_health", ""
    ).strip()

    comments = request.POST.get("comments", "").strip()

    
    visit_date = pending.get("visit_date")

    if not general_health or not comments:
        return JsonResponse({
            "success": False,
            "message": "Please complete all required assessment fields."
        }, status=400)

    if general_health not in ["Good", "Poor"]:
        return JsonResponse({
            "success": False,
            "message": "Select a valid general health status."
        }, status=400)

    if assessment_type == "general":

        on_drugs = request.POST.get("on_drugs", "").strip()

        if on_drugs not in ["Yes", "No"]:
            return JsonResponse({
                "success": False,
                "message": "Please indicate whether the patient is using drugs."
            }, status=400)

        payload = {
            "general_health": general_health,
            "on_drugs": on_drugs,
             "on_diet": "No",
            "comments": comments,
            "visit_date": visit_date,
            "patient_id": str(patient_id),
            "vital_id": str(pending["vital_id"]),
        }

    elif assessment_type == "overweight":

        on_diet = request.POST.get("on_diet", "").strip()

        if on_diet not in ["Yes", "No"]:
            return JsonResponse({
                "success": False,
                "message": "Please indicate whether the patient has been on a diet."
            }, status=400)

        payload = {
            "general_health": general_health,
            "on_diet": on_diet,
            "comments": comments,
            "on_drugs" : "No",
            "visit_date": visit_date,
            "patient_id": str(patient_id),
            "vital_id": str(pending["vital_id"]),
        }

    else:
        return JsonResponse({
            "success": False,
            "message": "Invalid assessment type."
        }, status=400)

    success, response_data = add_visit(
        access_token,
        payload
    )

    if not success:
        return JsonResponse({
            "success": False,
            "message": response_data.get(
                "message",
                "Unable to save the patient assessment."
            )
        }, status=400)

    
    del request.session["pending_assessment"]
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": "Patient assessment saved successfully.",
        "redirect": "/patient-list",
    })

def get_patient_visits(request):
    auth_user = request.session.get("auth_user")
    access_token = request.session.get("access_token")

    if not auth_user or not access_token:
        return redirect("login")

    if request.method != "POST":
        return redirect("getpatients")

    visit_date = request.POST.get("visit_date", "").strip()

    if not visit_date:
        messages.error(request, "Please select a visit date.")
        return redirect("getpatients")

    try:
        date.fromisoformat(visit_date)
    except ValueError:
        messages.error(request, "Please select a valid visit date.")
        return redirect("getpatients")

    success, response_data = get_visits_by_date(
        access_token,
        visit_date
    )

    if not success:
        messages.error(
            request,
            response_data.get("message", "Unable to retrieve patient visits.")
        )
        return redirect("getpatients")

    visits = response_data.get("data", [])

    return render(request, "patient-visits.html", {
        "auth_user": auth_user,
        "visits": visits,
        "visit_date": visit_date,
    })