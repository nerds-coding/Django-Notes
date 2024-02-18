import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from all_notes.models import Note, NotesVersionControl


# Create your views here.
@login_required
def create_new_note(request):

    try:
        status_code = 200
        msg = ""
        data = dict()
        logged_user = request.user
        if request.method == "POST":
            request_data = json.loads(request.body)

            title = request_data.get("title")
            content = request_data.get("content")

            if title or content:  # atleast one should have data to store
                note = Note(owner=logged_user)
                nvc = NotesVersionControl(
                    title=title, content=content, note=note, updated_by=logged_user
                )
                note.save()
                nvc.save()

                msg = "Notes created successfully"

            else:
                status_code = 400
                msg = "Atleast one field should contain data"
        else:
            status_code = 400  # bad request
            msg = "Invalid Request by client"
    except Exception as e:
        status_code = 401
        print(e)
        msg = str(e)

    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)


@login_required
def get_notes_data(request, id: int):
    status_code = 200
    msg = ""
    logged_user = request.user
    data = dict()

    # check that current user have permission to edit or not from shared or
    # he himself a owner

    if request.method == "GET":
        try:
            note = Note.objects.get(id=id)

            if not note.shared_with.filter(pk=logged_user.pk).exists() and logged_user!=note.owner:
                data = {
                    "message":"Current user don't have permission"
                }
                return JsonResponse(data=data, status=403)


            version_control_data = note.version_control.all()

            title = None
            content = None
            update_at = None

            for data in version_control_data:
                title = data.title
                content = data.content
                update_at = data.timestamp
                break

            data = {
                "title": title,
                "content": content,
                "updated_at": update_at,
                "owner": note.owner.email,
            }

            return JsonResponse(data=data, status=200)

        except Exception as e:
            status_code = 404
            print(str(e))
            msg = str(e)

    elif request.method == "PUT":
        request_data = json.loads(request.body)

        title = request_data.get("title")
        content = request_data.get("content")

        try:
            note = Note.objects.get(id=id)

            if not note.shared_with.filter(pk=logged_user.pk).exists() and logged_user!=note.owner:
                data = {
                    "message":"Current user don't have permission"
                }
                return JsonResponse(data=data, status=403)

            nvc = NotesVersionControl(
                title=title, content=content, note=note, updated_by=logged_user
            )
            nvc.save()

            msg = "Notes updated successfully"

        except Exception as e:
            status_code = 404
            print(str(e))
            msg = "Note doesn't Exists"
    else:
        status_code = 400  # bad request
        msg = "Invalid Request by client"

    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)


@login_required
def add_user_to_notes(request):
    status_code = 200
    msg = ""
    logged_user = request.user
    data = dict()
    if request.method == "POST":
        request_data = json.loads(request.body)

        shared_user_list = request_data.get("shared_user_list", [])
        note_id = request_data.get("note_id", 0)

        # to maintain the ACID property
        # if any of the user is not valid
        # then terminate the whole adding to shared list process
        flag = True
        share_user_email = None
        for users in shared_user_list:
            if not User.objects.filter(username=users).exists():
                flag = False
                share_user_email = users
                break

        if not flag:
            status_code = 404
            data = {"msg": f"{share_user_email} not found"}
            return JsonResponse(data=data, status=status_code)

        if shared_user_list:
            note = Note.objects.get(id=note_id)

            for users in shared_user_list:
                user_obj = User.objects.get(username=users)
                note.add_shared_user(user_obj)
                note.save()

            msg = "Note shared successfully"
        else:
            status_code = 400
            msg = "Shared user list can't be empty"
    else:
        status_code = 400  # bad request
        msg = "Invalid request"

    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)

@login_required
def notes_history(request, id: int):
    status_code = 200
    msg = ""
    logged_user = request.user
    data = dict()

    if request.method == "GET":
        try:
            note = Note.objects.get(id=id)

            version_control_data = note.version_control.all()

            title = None
            content = None
            update_at = None

            all_updates = dict()

            total_version = len(version_control_data)

            for idx,nvc_data in enumerate(version_control_data):
                title = nvc_data.title
                content = nvc_data.content
                update_at = nvc_data.timestamp,
                updated_by = nvc_data.updated_by

                all_updates[total_version] = dict(
                    title=title,
                    content=content,
                    updated_at=update_at,
                    updated_by=updated_by.username
                )
                total_version-=1
                

            return JsonResponse(data=all_updates, status=200)

        except Exception as e:
            status_code = 404
            print(str(e))
            msg = str(e)
    else:
        status_code = 400
        msg = "Invalid Request by client"

    data["msg"] = msg

    return JsonResponse(data=data, status=status_code)
