import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def employee_query(employee_id):
    try:
        # 檢查 Referer 標頭
        referer = frappe.local.request.headers.get('Referer')
        if not referer or not referer.startswith('http://163.18.26.149:5000'):
            return {
                "Status": "Error",
                "Msg": "Unauthorized access",
                "val": {}
            }

        # 查詢員工資料
        employee_records = frappe.get_all(
            "UCL_HR",
            filters={"employee_id": employee_id},
            fields=["employee_name", "employee_id", "department", "position", "email", "position_id"]
        )

        if not employee_records:
            return {
                "Status": "Error",
                "Msg": _("資料錯誤"),
                "val": {}
            }

        return {
            "Status": "Ok",
            "Msg": "身分查詢成功",
            "val": employee_records[0] if employee_records else {}
        }

    except Exception as e:
        return {
            "Status": "Error",
            "Msg": str(e),
            "val": {}
        }

@frappe.whitelist(allow_guest=True)
def staff_query(employee_id, position_id):
    try:
        # 檢查 Referer 標頭
        referer = frappe.local.request.headers.get('Referer')
        if not referer or not referer.startswith('http://163.18.26.149:5000'):
            return {
                "Status": "Error",
                "Msg": "Unauthorized access",
                "val": []
            }

        # 查詢使用者資料
        user_record = frappe.get_all(
            "UCL_HR",
            filters={"employee_id": employee_id},
            fields=["employee_id"]
        )

        if not user_record:
            return {
                "Status": "Error",
                "Msg": _("使用者資料錯誤"),
                "val": []
            }

        employee_records = frappe.get_all(
            "UCL_HR",
            filters={"position_id": position_id},
            fields=["employee_name", "employee_id", "department", "position", "email", "position_id"]
        )

        if not employee_records:
            return {
                "Status": "Error",
                "Msg": _("找不到符合該職位的員工"),
                "val": []
            }

        return {
            "Status": "Ok",
            "Msg": "查詢成功",
            "val": employee_records
        }

    except Exception as e:
        return {
            "Status": "Error",
            "Msg": str(e),
            "val": []
        }
