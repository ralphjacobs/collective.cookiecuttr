from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import getToolByName

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.cookiecuttr.interfaces import ICookieCuttrSettings


class CookieCuttrViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(CookieCuttrViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        registry = getUtility(IRegistry)
        try:
            self.settings = registry.forInterface(ICookieCuttrSettings)
        except KeyError:
            self.settings = None

    def update(self):
        pass

    def available(self):
        if not self.settings:
            return False
        if self.settings.cookiecuttr_enabled:
            return True
        return False

    def render(self):
        if self.available():
            root = getToolByName(self, 'portal_url')
            root = root.getPortalObject()
            try:
                location = root.restrictedTraverse(str(self.settings.link))
                link = location.absolute_url()
            except:
                link = ''
            snippet = safe_unicode(js_template % (link,
                                                  self.settings.text,
                                                  self.settings.accept_button))
            return snippet
        return ""

js_template = """
<script type="text/javascript">

    (function($) {
        $(document).ready(function () {
            $.cookieCuttr({cookieAnalytics: false,
                           cookiePolicyLink: "%s",
                           cookieMessage: "%s",
                           cookieAcceptButtonText: "%s",
                           });
        })
    })(jQuery);
</script>

"""
