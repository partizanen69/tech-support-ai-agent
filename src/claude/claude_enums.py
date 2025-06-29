from enum import Enum


class TicketCategory(Enum):
    AUTHENTICATION_AND_ACCESS_MANAGEMENT = "Аутентифікація та керування доступом"
    BILLING = "Керування рахунками та оплатами"
    TROUBLESHOOTING = "Розв'язання технічних проблем"
    GENERAL = "Всі інші питання"
