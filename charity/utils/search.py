from django.db.models import Q

def search_by_title_or_tag(queryset, title=None, tag=None, tag_field='tags__name'):
    if not title and not tag:
        return queryset.none()
    if title and tag:
        queryset = queryset.filter(
            Q(title__icontains=title) | Q(**{f"{tag_field}__icontains": tag}) #__icontains to make it canse not sensitive
        )
    elif title:
        queryset = queryset.filter(title__icontains=title)
    elif tag:
        queryset = queryset.filter(**{f"{tag_field}__icontains": tag})
    return queryset.distinct()