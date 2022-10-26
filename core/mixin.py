from django.http import Http404

#Custom Permission
class ClaimerUserOnlyMixin(object):

    prefix = 'claimer'

    def has_permissions(self):
        # Assumes that your User request has a type key called `claimer`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(ClaimerUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class DefendantUserOnlyMixin(object):

    prefix = 'defendant'

    def has_permissions(self):
        # Assumes that your User request has a type key called `defendant`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(DefendantUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class ArbitratorUserOnlyMixin(object):

    prefix = 'arbitrator'

    def has_permissions(self):
        # Assumes that your User request has a type key called `arbitrator`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(ArbitratorUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class WitnessUserOnlyMixin(object):

    prefix = 'witness'

    def has_permissions(self):
        # Assumes that your User request has a type key called `witness`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(WitnessUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class RespondantUserOnlyMixin(object):

    prefix = 'respondant'

    def has_permissions(self):
        # Assumes that your User request has a type key called `respondant`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(RespondantUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class CreatorUserOnlyMixin(object):

    prefix = 'creator'

    def has_permissions(self):
        # Assumes that your User request has a type key called `creator`.
        return self.prefix == self.request.user.type

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(CreatorUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)

