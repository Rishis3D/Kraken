"""Kraken - objects.Attributes.attribute_group module.

Classes:
AttributeGroup - Attribute Group.

"""

from kraken.core.objects.scene_item import SceneItem


class AttributeGroup(SceneItem):
    """Attribute Group that attributes belong to."""

    def __init__(self, name, parent=None):
        super(AttributeGroup, self).__init__(name)
        self._attributes = []

        if parent is not None:
            if 'Object3D' not in parent.getTypeHierarchyNames():
                raise ValueError("Parent: " + parent.getName() +
                    " is not of type 'Object3D'!")

            parent.addAttributeGroup(self)


    # =============
    # Name Methods
    # =============
    def getDecoratedPath(self):
        """Gets the decorated path of the object.

        Return:
        String, decorated path  of the object.

        """

        if self.getParent() is not None and not self.getParent().isTypeOf('Component'):
            return self.getParent().getDecoratedPath() + '.' + ':' + self.getName()

        return self.getName()


    # ==================
    # Attribute Methods
    # ==================
    def checkAttributeIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, attribute index to check.

        Return:
        True if successful.

        """

        if index > len(self._attributes):
            raise IndexError("'" + str(index) + "' is out of the range of 'attributes' array.")

        return True


    def addAttribute(self, attribute):
        """Adds an attribute to this object.

        Arguments:
        attribute -- Object, attribute object to add to this object.

        Return:
        True if successful.

        """

        if attribute.getName() in [x.getName() for x in self._attributes]:
            raise IndexError("Child with " + attribute.getName() + " already exists as a attribute.")

        self._attributes.append(attribute)
        attribute.setParent(self)

        return True


    def removeAttributeByIndex(self, index):
        """Removes attribute at specified index.

        Arguments:
        index -- Integer, index of attribute to remove.

        Return:
        True if successful.

        """

        if self.checkAttributeIndex(index) is not True:
            return False

        del self._attributes[index]

        return True


    def removeAttributeByName(self, name):
        """Removes the attribute with the specified name.

        Arguments:
        name -- String, name of the attribute to remove.

        Return:
        True if successful.

        """

        removeIndex = None

        for i, eachAttribute in enumerate(self._attributes):
            if eachAttribute.getName() == name:
                removeIndex = i

        if removeIndex is None:
            return False

        self.removeAttributeByIndex(removeIndex)

        return True


    def getNumAttributes(self):
        """Returns the number of attributes as an integer.

        Return:
        Integer of the number of attributes on this object.

        """

        return len(self._attributes)


    def getAttributeByIndex(self, index):
        """Returns the attribute at the specified index.

        Arguments:
        index -- Integer, index of the attribute to return.

        Return:
        Attribute at the specified index.
        False if not a valid index.

        """

        if self.checkAttributeIndex(index) is not True:
            return False

        return self._attributes[index]


    def getAttributeByName(self, name):
        """Return the attribute with the specified name.

        Arguments:
        name -- String, name of the attribute to return.

        Return:
        Attribute with the specified name.
        None if not found.

        """

        for eachAttribute in self._attributes:
            if eachAttribute.getName() == name:
                return eachAttribute

        return None


    # ====================
    # Persistence Methods
    # ====================
    def jsonEncode(self, saver):
        """Returns the data for this object encoded as a JSON hierarchy.

        Arguments:

        Return:
        A JSON structure containing the data for this SceneItem.

        """

        classHierarchy = []
        for cls in type.mro(type(self)):
            if cls == object:
                break;
            classHierarchy.append(cls.__name__)

        jsonData = {
            '__typeHierarchy__': classHierarchy,
            'name': self.name,
            'parent': self.getParent().getName(),
            'attributes': []
        }
        for attr in self._attributes:
            jsonData['attributes'].append(attr.jsonEncode(saver))

        return jsonData


    def jsonDecode(self, loader, jsonData):
        """Returns the color of the object.

        Return:
        the decoded object.

        """

        for attr in jsonData['attributes']:
            self.addAttribute(loader.construct(attr))

        return True