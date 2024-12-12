from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from .backend_functions import transcribe_audio1, extract_text_from_pdf, extract_main_text, get_answer
import json
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


def land_page(request):
    return render(request, 'landingpage.html')


def how_to_use(request):
    return render(request, 'howtouse.html')

def faq(request):
    return render(request, 'faq.html')


@login_required
def history_view(request):
    user_chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'chats': user_chats})


@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile

        user.first_name = request.POST.get("first_name", user.first_name)
        profile.location = request.POST.get("location", profile.location)
        profile.occupation = request.POST.get("occupation", profile.occupation)

        if "profile_picture" in request.FILES:
            profile.profile_picture = request.FILES["profile_picture"]

        user.save()
        profile.save()

        return redirect("profile")

    return render(request, "profile.html", {"user": request.user})




def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a profile for the user
            profile = Profile.objects.create(user=user)

            # Save profile picture if provided
            if "profile_picture" in request.FILES:
                profile.profile_picture = request.FILES["profile_picture"]
                profile.save()

            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})





@login_required
def chat_home(request):
    return render(request, 'chat.html')


from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def process_query(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get('question', '')
        context = data.get('context', '')

        # # Log for debugging
        # logger.info(f"Received context: {context[:50]}...")
        # logger.info(f"Received question: {user_input}")

        # Generate the bot's response
        bot_response = get_answer(context, user_input)
        logger.info(f"Bot response: {bot_response}")

        # Save the chat, associating it with the logged-in user
        chat = Chat(user_input=user_input, bot_response=bot_response, context=context, user=request.user)
        chat.save()

        return JsonResponse({"bot_response": bot_response, "chat_id": str(chat.id)})



@login_required
def fetch_chat_history(request):
    if request.method == "GET":
        chats = Chat.objects.filter(user=request.user).order_by("-created_at")  # Filter by user
        chat_history = [
            {
                "id": str(chat.id),
                "user_input": chat.user_input,
                "bot_response": chat.bot_response,
                "created_at": chat.created_at,
            }
            for chat in chats
        ]
        return JsonResponse({"chat_history": chat_history})



def view_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat.id)
        return JsonResponse({
            "id": str(chat.id),
            "user_input": chat.user_input,
            "bot_response": chat.bot_response,
            "context": chat.context,
            "created_at": chat.created_at,
        })
    except Chat.DoesNotExist:
        return JsonResponse({"error": "Chat not found"}, status=404)

@csrf_exempt
def extract_text_from_url(request):
    if request.method == "POST":
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            url = data.get('url', '')

            if not url:
                return JsonResponse({"error": "No URL provided"}, status=400)

            # Simulated extracted text (replace with actual extraction logic)
            extracted_text = extract_main_text(url)

            return JsonResponse({"text": extracted_text}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def extract_text_from_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file')

        if uploaded_file.content_type == "application/pdf":
            # Save the uploaded file temporarily
            with open(uploaded_file.name, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(temp_file.name)
            return JsonResponse({"text": extracted_text})
        else:
            return JsonResponse({"error": "Unsupported file type"}, status=400)

@csrf_exempt
def transcribe_audio(request):
    if request.method == "POST":
        audio_file = request.FILES.get('audio')

        # Save the audio file temporarily
        with open(audio_file.name, 'wb') as temp_audio:
            for chunk in audio_file.chunks():
                temp_audio.write(chunk)

        # Transcribe the audio to text
        transcribed_text = transcribe_audio1(temp_audio.name)
        return JsonResponse({"text": transcribed_text})

# @csrf_exempt
# def transcribe_audio(request):
#     if request.method == "POST":
#         audio_file = request.FILES.get("audio")

#         if not audio_file:
#             return JsonResponse({"error": "No audio file provided"}, status=400)

#         try:
#             # Save the audio file temporarily
#             temp_audio_path = f"/tmp/{audio_file.name}"
#             with open(temp_audio_path, "wb") as temp_audio:
#                 for chunk in audio_file.chunks():
#                     temp_audio.write(chunk)

#             # Transcribe the audio to text
#             transcribed_text = transcribe_audio1(temp_audio_path)
#             return JsonResponse({"text": transcribed_text})

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def set_paragraph_context(request):
    if request.method == "POST":
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            paragraph = data.get("paragraph", "").strip()

            if not paragraph:
                return JsonResponse({"error": "No paragraph provided"}, status=400)

            # Simulate storing or processing the paragraph
            # (In a real app, you might save this in a session or database)
            return JsonResponse({"message": "Context set successfully", "context": paragraph}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)