import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def employee_query(employee_id):
    try:
        # 根据员工ID查询员工资料
        employee_records = frappe.get_all(
            "UCL_HR",  # 使用 DocType 名称
            filters={"employee_id": employee_id},
            fields=["employee_name", "employee_id", "department", "position", "email", "position_id"]
        )

        # 如果没有找到符合条件的记录，返回错误信息
        if not employee_records:
            return {
                "Status": "Error",
                "Msg": _("资料错误"),
                "val": {}
            }

        # 处理返回的员工记录
        employee_info = []
        for record in employee_records:
            employee_info.append({
                "userId": record.get("employee_id"),
                "name": record.get("employee_name"),
                "Role": record.get("position"),
                "email": record.get("email"),
                "department": record.get("department"),
                "positionId": record.get("position_id")
            })

        return {
            "Status": "Ok",
            "Msg": _("身份查询成功"),
            "val": employee_info
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
        # 根据用户的员工ID查询是否存在
        user_record = frappe.get_all(
            "UCL_HR",  # 使用 DocType 名称
            filters={"employee_id": employee_id},
            fields=["employee_id"]
        )

        # 如果用户的员工ID不存在，返回错误信息
        if not user_record:
            return {
                "Status": "Error",
                "Msg": _("用户资料错误"),
                "val": []
            }

        # 根据希望查询的职位返回所有符合条件的员工资料
        employee_records = frappe.get_all(
            "UCL_HR",  # 使用 DocType 名称
            filters={"position_id": position_id},
            fields=["employee_name", "employee_id", "department", "position", "email", "position_id"]
        )

        # 如果没有找到符合条件的记录，返回提示信息
        if not employee_records:
            return {
                "Status": "Error",
                "Msg": _("找不到符合该职位的员工"),
                "val": []
            }

        # 构建返回结果
        formatted_records = [
            {
                "userId": record.get("employee_id"),
                "name": record.get("employee_name"),
                "Role": record.get("position"),
                "email": record.get("email"),
                "department": record.get("department"),
                "positionId": record.get("position_id")
            }
            for record in employee_records
        ]

        return {
            "Status": "Ok",
            "Msg": _("查询成功"),
            "val": formatted_records
        }

    except Exception as e:
        return {
            "Status": "Error",
            "Msg": str(e),
            "val": []
        }

