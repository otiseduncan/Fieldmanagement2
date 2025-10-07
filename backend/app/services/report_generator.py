from __future__ import annotations

from datetime import datetime
from typing import Any

from jinja2 import Template

REPORT_TEMPLATE = Template(
    """
    FieldService 2 Report
    =====================
    Job ID: {{ job.id }}
    RO Number: {{ job.ro_number }}
    VIN: {{ job.vin }}
    Technician Notes: {{ job.technician_notes or 'N/A' }}
    Generated At: {{ generated_at }}
    """
)


def generate_job_report(job: Any) -> str:
    """Render a simple text report for a job instance."""
    return REPORT_TEMPLATE.render(job=job, generated_at=datetime.utcnow())
