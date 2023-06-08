from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Piupiu

# Desregistrar os Grupos existentes no sistema de autenticação padrão do Django.
# Neste caso, estamos removendo a funcionalidade de agrupamento de usuários.
admin.site.unregister(Group)

# Criar uma classe "ProfileInline" para representar o perfil do usuário dentro da página de administração.
# Essa classe é usada para mesclar as informações do perfil do usuário com as informações do usuário.
class ProfileInline(admin.StackedInline):
	model = Profile

# Criar uma classe "UserAdmin" para personalizar a exibição do modelo User na página de administração.
# Aqui definimos quais campos serão exibidos e também incluímos o perfil do usuário.
class UserAdmin(admin.ModelAdmin):
	model = User
	# Definir os campos que serão exibidos para cada usuário.
	fields = ["username"]
	# Incluir a classe ProfileInline para exibir as informações do perfil do usuário.
	inlines = [ProfileInline]

# Desregistrar o modelo User padrão do Django para permitir a personalização.
admin.site.unregister(User)

# Registrar novamente o modelo User e o modelo Profile, mas com as personalizações definidas anteriormente.
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

# Registrar o modelo Piupiu para que ele possa ser gerenciado pela página de administração.
# Os Piupius são objetos que representam as mensagens publicadas pelos usuários.
admin.site.register(Piupiu)
