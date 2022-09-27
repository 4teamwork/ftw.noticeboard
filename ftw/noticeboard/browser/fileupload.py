from AccessControl import getSecurityManager
from plone import api
from plone.app.content.browser.file import FileUploadView
from plone.namedfile.file import NamedBlobImage
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.permissions import AddPortalContent
from Products.CMFPlone.utils import safe_unicode
import json
import mimetypes


class ImageUploadView(FileUploadView):
    """ Copy of the original, but we want a different type and no tus and no
    AT support"""
    def __call__(self):
        # Check if user has permission to add content here
        sm = getSecurityManager()
        if not sm.checkPermission(AddPortalContent, self.context):
            response = self.request.RESPONSE
            response.setStatus(403)
            return "You are not authorized to add content to this folder."

        req = self.request
        if req.REQUEST_METHOD != 'POST':
            return
        filedata = self.request.form.get("file", None)
        if filedata is None:
            return
        filename = safe_unicode(filedata.filename)

        if not filedata:
            return

        type_ = 'ftw.noticeboard.NoticeImage'

        # Now check that the object is not restricted to be added in the
        # current context
        allowed_ids = [
            fti.getId() for fti in self.context.allowedContentTypes()
        ]
        if type_ not in allowed_ids:
            response = self.request.RESPONSE
            response.setStatus(403)
            if type_ == 'File':
                return "You cannot add a File to this folder, try another one"
            if type_ == 'Image':
                return (
                    "You cannot add an Image to this folder, "
                    "try another one"
                )

        content_type = mimetypes.guess_type(filename)[0] or ""
        image = NamedBlobImage(data=filedata,
                               contentType=content_type,
                               filename=filename)
        obj = api.content.create(container=self.context,
                                 type=type_,
                                 title=filename,
                                 safe_id=True,
                                 image=image)

        result = {
            "type": '',
            "size": 0
        }

        result['size'] = obj.image.getSize()
        result['type'] = obj.image.contentType

        result.update({
            'url': obj.absolute_url(),
            'name': obj.getId(),
            'UID': IUUID(obj),
            'filename': filename
        })

        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8'
        )
        return json.dumps(result)
