from functional.functional_tools.composing import (
    ExecutionContext,
    Issue,
    IssueType,
    bind,
    bind_all,
)
from functional.mail_workflow.mail_message_core import (
    MailMessage,
    RunEnvironment,
    log_issues,
    send_message_utility,
    validate_message_utility,
)

EmailContext = ExecutionContext[MailMessage, RunEnvironment]


def validation_step(context: EmailContext) -> EmailContext:
    errors = validate_message_utility(context.payload)
    return context.with_issues(
        new_issues=[
            Issue(issue_type=IssueType.ERROR, message=message) for message in errors
        ]
    )


def log_step(context: EmailContext) -> EmailContext:
    log_errors = log_issues(
        run_environment=context.environment,
        log_messages=[
            f"{issue.issue_type.value}: {issue.message}" for issue in context.issues
        ],
    )

    return context.with_issues(
        new_issues=[
            Issue(issue_type=IssueType.ERROR, message=message) for message in log_errors
        ]
    )


def send_step(context: EmailContext) -> EmailContext:
    send_errors = send_message_utility(
        run_environment=context.environment, mail_message=context.payload
    )
    return context.with_issues(
        new_issues=[
            Issue(issue_type=IssueType.ERROR, message=message)
            for message in send_errors
        ]
    )


# pylint: disable=duplicate-code
def send_mail_functional(
    sender: str, recipient: str, subject: str, text: str
) -> EmailContext:
    mail_message = MailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        text=text,
    )

    run_environment: RunEnvironment = RunEnvironment(
        smtp_server="my-server", log_file="./log.txt"
    )

    context: EmailContext = EmailContext(
        environment=run_environment,
        payload=mail_message,
    )

    validation_logged = bind(validation_step, log_step)

    message_sent = bind(validation_logged, send_step)

    final = bind(message_sent, log_step)

    return final(context=context)


# pylint: disable=duplicate-code
def send_mail_via_bind_all(
    sender: str, recipient: str, subject: str, text: str
) -> EmailContext:
    mail_message = MailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        text=text,
    )

    run_environment: RunEnvironment = RunEnvironment(
        smtp_server="my-server", log_file="./log.txt"
    )

    context: EmailContext = EmailContext(
        environment=run_environment,
        payload=mail_message,
    )

    compound = bind_all([validation_step, log_step, send_step, log_step])

    return compound(context=context)


# pylint: disable=duplicate-code
if __name__ == "__main__":
    print("===== CASE1: (Errors)")
    print(
        send_mail_functional(
            sender="myself",
            recipient="destination@some.address",
            subject="A Subject",
            text="A Message...",
        )
    )

    print("===== CASE2: (Ok)")
    print(
        send_mail_functional(
            sender="myself@my.address",
            recipient="destination@some.address",
            subject="A Subject",
            text="A Message...",
        )
    )

    print("===== CASE3: (Ok / bind all)")
    print(
        send_mail_via_bind_all(
            sender="myself@my.address",
            recipient="destination@some.address",
            subject="A Subject",
            text="A Message...",
        )
    )
