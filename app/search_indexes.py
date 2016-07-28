import datetime
from haystack import indexes
from app.models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text=indexes.CharField(document=True, use_template=True)
    start_date=indexes.DateTimeField(model_attr='start_time')
    title=indexes.CharField(model_attr='title')

    content_auto=indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Event
    
    def index_queryset(self, using=None):
    
        return self.get_model().objects.all()