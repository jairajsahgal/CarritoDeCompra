from django.db.models import Manager, QuerySet, Q


class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)


class ForCart(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(Q(cap__is_deleted=True)|Q(tshirt__is_deleted=True))
