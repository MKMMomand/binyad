from django.core.management.base import BaseCommand
from apps.core.models import SiteSettings, FAQ
from apps.services.models import Service
from apps.products.models import Product


class Command(BaseCommand):
    help = "Seed development demo content. Run only in development."

    def handle(self, *args, **options):
        SiteSettings.load()
        services = [
            ("Website Development", "طراحی وب‌سایت", "bi-globe"),
            ("Business Management Systems", "سیستم‌های مدیریتی", "bi-briefcase"),
            ("Database Development", "بانک اطلاعاتی", "bi-database"),
            ("Office Administration Systems", "مدیریت دفاتر", "bi-building"),
            ("Custom Software", "نرم‌افزارهای اختصاصی", "bi-code-slash"),
            ("Mobile Applications", "اپلیکیشن موبایل", "bi-phone"),
            ("Inventory & Warehouse Systems", "سیستم‌های گدام و انبار", "bi-box-seam"),
            ("Customer Management Systems", "سیستم مدیریت مشتریان", "bi-people"),
            ("Employee & HR Systems", "سیستم‌های کارمندان و منابع بشری", "bi-person-badge"),
            ("IT Consulting", "مشاوره تکنالوژی معلوماتی", "bi-lightbulb"),
            ("Digitalization", "دیجیتال‌سازی", "bi-arrow-repeat"),
            ("Offline Software", "نرم‌افزارهای آفلاین", "bi-hdd-network"),
        ]
        for i, (en, fa, icon) in enumerate(services):
            Service.objects.update_or_create(
                name=en,
                defaults=dict(name_fa=fa, name_en=en, icon=icon, active=True, order=i)
            )
        products = [
            ("Binyad Office", "بنیاد آفیس", Product.Status.IN_DEVELOPMENT, "مدیریت کارمندان، اسناد، مکاتیب، گزارش‌ها"),
            ("Binyad Inventory", "بنیاد انوانتری", Product.Status.PLANNED, "مدیریت گدام و موجودی"),
            ("Binyad CRM", "بنیاد مدیریت مشتریان", Product.Status.PLANNED, "مدیریت ارتباط با مشتریان"),
            ("Binyad HR", "بنیاد منابع بشری", Product.Status.PLANNED, "منابع بشری و حاضری"),
            ("Binyad Property", "بنیاد املاک", Product.Status.PLANNED, "مدیریت املاک و اجاره"),
            ("Binyad School", "بنیاد مکتب", Product.Status.PLANNED, "سیستم مدیریت مکتب"),
            ("Binyad Clinic", "بنیاد کلینیک", Product.Status.PLANNED, "سیستم مدیریت کلینیک"),
        ]
        for i, (en, fa, status, desc) in enumerate(products):
            Product.objects.update_or_create(
                name=en,
                defaults=dict(name_fa=fa, name_en=en, status=status,
                              short_description_fa=desc, short_description_en=desc, order=i)
            )
        self.stdout.write(self.style.SUCCESS("Demo data seeded."))