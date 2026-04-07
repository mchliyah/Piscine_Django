from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import InputHistoryForm


def _get_log_path() -> Path:
    return Path(settings.EX02_LOG_PATH)


def _append_log_entry(user_text: str, submitted_at: datetime) -> None:
    log_path = _get_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{submitted_at.isoformat()} {user_text}\n")


def _read_history() -> list[dict[str, str]]:
    log_path = _get_log_path()
    if not log_path.exists():
        return []

    history: list[dict[str, str]] = []
    with log_path.open("r", encoding="utf-8") as log_file:
        for line in log_file:
            entry = line.rstrip("\n")
            if not entry:
                continue
            if " " in entry:
                timestamp_raw, text = entry.split(" ", 1)
            else:
                timestamp_raw, text = entry, ""

            try:
                timestamp = datetime.fromisoformat(timestamp_raw)
                timestamp_display = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp_display = timestamp_raw

            history.append({"timestamp": timestamp_display, "text": text})

    return history


def ex02_page(request):
    if request.method == "POST":
        form = InputHistoryForm(request.POST)
        if form.is_valid():
            submitted_at = timezone.now()
            user_text = form.cleaned_data["text"]
            _append_log_entry(user_text=user_text, submitted_at=submitted_at)
            return redirect("ex02-page")
    else:
        form = InputHistoryForm()

    context = {
        "form": form,
        "history": _read_history(),
    }
    return render(request, "ex02.html", context)
