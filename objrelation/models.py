from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from renoauth.models import *
from message.models import *
from django.utils.timezone import now


@python_2_unicode_compatible
class MessageReact(models.Model):
    message = models.ForeignKey('message.models.Message', related_name='friend_from')
    _from = models.ForeignKey(UserExtension, related_name='friend_to')
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "from %s to %s" % (self._from.usersubusername.username, self._to.usersubusername.username)

    class Meta:
        unique_together = ('message', '_from',)


@python_2_unicode_compatible
class MessageRead(models.Model):
    message = models.ForeignKey(Message, related_name='friend_from')
    _from = models.ForeignKey(UserExtension, related_name='friend_to')

    def __str__(self):
        return "from %s to %s" % (self._from.usersubusername.username, self._to.usersubusername.username)

    class Meta:
        unique_together = ('message', '_from',)


@python_2_unicode_compatible
class MessageRemove(models.Model):
    message = models.ForeignKey(Message)
    _from = models.ForeignKey(UserExtension, related_name='follow_from')
    created = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=True)
    double = models.BooleanField(default=False)

    def __str__(self):
        return "from %s to %s" % (self._from.usersubusername.username, self._to.usersubusername.username)

    class Meta:
        unique_together = ('message', '_from',)


@python_2_unicode_compatible
class News(models.Model):
    user_extension = models.OneToOneField(UserExtension)
    viewed = models.DateTimeField(default=now())
    count = models.PositiveSmallIntegerField(default=0)


@python_2_unicode_compatible
class NewsSource(models.Model):
    news = models.ForeignKey(News)
    status = models.PositiveSmallIntegerField(default=0)


@python_2_unicode_compatible
class NewsSourceFollowFrom(models.Model):
    user_extension = models.ForeignKey(UserExtension)


@python_2_unicode_compatible
class NewsSourceFriendsWith(models.Model):
    user_extension = models.ForeignKey(UserExtension)


@python_2_unicode_compatible
class NewsSourceReactionTo(models.Model):
    user_extension = models.ForeignKey(UserExtension)
    message = models.ForeignKey(Message)

# ----------------------------------------------------------------------------------------------------------------------


@python_2_unicode_compatible
class PageExtension(models.Model):


@python_2_unicode_compatible
class PageUri(models.Model):
    uri = models.TextField(max_length=202)
    page_extension = models.OneToOneField(PageExtension)


@python_2_unicode_compatible
class PageRefreshUri(models.Model):
    page_extension = models.ForeignKey(PageExtension, related_name='page_extension')
    destination_uri = models.ForeignKey(PageExtension, related_name='destination_uri')
    refresh_time = models.PositiveSmallIntegerField(default=0)

class PageSearchWordList(models.Model):
    page_extension = models.OneToOneField(PageExtension)


class PageSearchWordListSource(models.Model):
    page_search_word_list = models.ForeignKey(PageSearchWordList)
    simple_search_word_extension = models.ForeignKey('objectrelation.models.SimpleSearchWordExtension')


# Search Word Things
@python_2_unicode_compatible
class SimpleSearchWord(models.Model):
    simple_search_word = models.TextField(max_length=20)

class SimpleSearchWordExtension(models.Model):
    simple_search_word = models.OneToOneField(SimpleSearchWord)

class SimpleSearchWordRemovable(models.Model):
    simple_search_word = models.OneToOneField(SimpleSearchWord)
    removable = models.BooleanField(default=True)

class SimpleSearchWordModified(models.Model):
    simple_search_word = models.ForeignKey(SimpleSearchWord)
    user_extension = models.ForeignKey(UserExtension)
    modified_search_word = models.TextField(max_length=20)

class SimpleSearchWordModifiedPro(models.Model):
    simple_search_word_modified = models.ForeignKey(SimpleSearchWordModified)
    user_extension = models.ForeignKey(UserExtension)

class SimpleSearchWordModifiedProSum(models.Model):
    simple_search_word_modified = models.ForeignKey(SimpleSearchWordModified)
    sum = models.CharField(max_length=5)

class SimpleSearchWordPageList(models.Model):
    simple_search_word_extension = models.OneToOneField(SimpleSearchWordExtension)


class SimpleSearchWordPageSource(models.Model):
    simple_search_word_page_list = models.ForeignKey(SimpleSearchWordPageList)
    page_extension = models.ForeignKey(PageExtension)

class SimpleSearchWordPageSourceRemovable(models.Model):
    removable = models.BooleanField(default=True)
    simple_search_word_page_source = models.ForeignKey(SimpleSearchWordPageSource)

class SimpleSearchWordPageSourceTitle(models.Model):
    user_extension = models.ForeignKey(UserExtension)
    title = models.ForeignKey(SimpleSearchWordPageSource)

class SimpleSearchWordPageSourceTitleRemovable(models.Model):
    removable = models.BooleanField(default=True)
    simple_search_word_page_source_title = models.ForeignKey(SimpleSearchWordPageSourceTitle)


class SimpleSearchWordPageSourceFit(models.Model):
    simple_search_word_page_source = models.ForeignKey(SimpleSearchWordPageSource)
    fit = models.BooleanField(default=True)
    user_extension = models.ForeignKey(UserExtension)

class SimpleSearchWordPageSourceFitSum(models.Model):
    simple_search_word_page_source = models.ForeignKey(SimpleSearchWordPageSource)
    sum = models.CharField(max_length=5)


class SimpleSearchWordPageSourceTitleProSum(models.Model):
    simple_search_word_page_source_title = models.ForeignKey(SimpleSearchWordPageSourceTitle)
    sum = models.CharField(max_length=5)

class SimpleSearchWordPageSourceTitlePro(models.Model):
    simple_search_word_page_source_title = models.ForeignKey(SimpleSearchWordPageSourceTitle)
    user_extension = models.ForeignKey(UserExtension)

# Private Things
class PrivateExtension(models.Model):
    user_extension = models.OneToOneField(UserExtension)


@python_2_unicode_compatible
class PrivatePageUri(models.Model):
    uri = models.TextField(max_length=202)

class PrivatePageExtension(models.Model):
    private_page_uri = models.OneToOneField(PrivatePageUri)

class PrivatePageTitle(models.Model):


class PrivateRefreshUri(models.Model):
    private_page_extension = models.ForeignKey(PrivatePageExtension)
    destination_uri = models.ForeignKey(PrivatePageExtension, related_name='destination_uri')
    refresh_time = models.PositiveSmallIntegerField(default=0)


class PrivatePageSearchWordList(models.Model):
    private_page_extension = models.OneToOneField(PrivatePageExtension)


class PrivatePageSearchWordListSource(models.Model):
    private_page_search_word_list = models.ForeignKey(PrivatePageSearchWordList)
    simple_search_word_extension = models.ForeignKey('objectrelation.models.SimpleSearchWordExtension')


# Search Word Things
@python_2_unicode_compatible
class PrivateSimpleSearchWord(models.Model):
    simple_search_word = models.TextField(max_length=20)

class PrivateSimpleSearchWordExtension(models.Model):
    private_simple_search_word = models.OneToOneField(PrivateSimpleSearchWord)

class PrivateSimpleSearchWordPageList(models.Model):
    simple_search_word_extension = models.OneToOneField(SimpleSearchWordExtension)

class PrivateSimpleSearchWordPageSource(models.Model):
    simple_search_word_page_list = models.ForeignKey(SimpleSearchWordPageList)
    page_extension = models.ForeignKey(PageExtension)

# 나머지 다른 설정들 fit없으면 삭제 이런것은 계정 공개시 모두 등록되는걸로 하고 비공개시만 비공개로 한 포스트로 변경되며 비공개로
# 등록할 순 없고 공개로 등록하고 비공개로 전환 가능하도록 하고 undeleted 옵션을 만들자.
# private 에서 한거랑 fit를 분리하자. 자동 fit 없도록. 등록만 되도록. 그리고 기본적으로 공적인 자료에선 삭제도 없다.
# fitness 와 reaction, comments 만 있음.
# 어차피 private 으로부터 search word 시작이니 search word 삭제도 별 의미 없다. 등록될 뿐으로 해도 될 것 같다.
# flow는 포린키 이용해서 새 글처럼. 필터를 어쩔 수 없이 써야할 것 같다 . 하이드기능 바모울에도 넣기

# 레이메이에서 공유하기는 포린키 + 새 메시지 로 구현가능하다.

# 뷰 단에서 하도록 하고 일단은 너무 복잡하게 만들지 말자 구조를.