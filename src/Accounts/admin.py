from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile

class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "role", "is_staff", "is_active", "created_at")
    list_filter = ("role", "is_staff", "is_active", "created_at")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Roles", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )

    readonly_fields = ("created_at",)  # Rend le champ visible mais non modifiable

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "student_id", "parcours")
    search_fields = ("user__username", "student_id", "parcours")
    ordering = ("id",)

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "teacher_id", "matiere")
    search_fields = ("user__username", "teacher_id", "matiere")
    ordering = ("id",)

# Enregistrement des modèles dans l'admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
