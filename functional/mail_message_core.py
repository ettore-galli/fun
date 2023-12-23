from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List


@dataclass(frozen=True)
class RunEnvironment:
    smtp_server: str
    log_file: str


@dataclass(frozen=True)
class MailMessage:
    sender: str
    recipient: str
    subject: str
    text: str


def validate_message_utility(mail_message: MailMessage) -> List[str]:
    issues: List[str] = []

    if "@" not in mail_message.sender:
        issues.append("Sender mail not valid")
    if "@" not in mail_message.recipient:
        issues.append("Recipient mail not valid")
    if len(mail_message.subject) == 0:
        issues.append("Subject is mandatory")
    return issues


def send_message_utility(
    run_environment: RunEnvironment, mail_message: MailMessage
) -> List[str]:
    if run_environment.smtp_server == "":
        return ["No server"]
    print(
        f"Sending message {mail_message.subject} {mail_message.text} "
        "from {mail_message.sender} "
        "to {mail_message.recipient} "
        "via server {run_environment.smtp_server}"
    )

    return []


def log_issues(
    run_environment: RunEnvironment, log_messages: Iterable[str]
) -> List[str]:
    if run_environment.log_file == "":
        return ["No log file"]
    try:
        with open(run_environment.log_file, "w", encoding="utf-8") as logfile:
            for line in log_messages:
                logfile.write(f"{datetime.now()}: {line}\n")
    except Exception as error:  # pylint: disable=broad-exception-caught
        return [str(error)]

    return []
