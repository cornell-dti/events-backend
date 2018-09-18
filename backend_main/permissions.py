from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	'''
		Custom permission to allow only owners of an object to edit
	'''
	
	def has_object_permission(self, request, view, obj):
		#Read permissions are allowed to any request
		#always allow GET, HEAD, or OPTIONS
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner == request.user