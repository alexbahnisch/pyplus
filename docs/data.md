A collection of data driven object mixins and decorators.

## DataObjectMixin()
A mixin to create data driven objects that can be easily serialized and deserialized.
If used as super class, subclass must override '\_\_HEADER\_\_' attribute with a list of strings that represent an
ordered dict key to '\_\_init\_\_' arg mapping.

### from_dict(arg)
Deserialize object from a dict.

#### arguments
* **arg** *{dict}*

#### return
* *{pyplus.data.DataObjectMixin}*

### from_line(line)
Deserialize object from a line of text. Needs to be overridden to be used.

#### arguments
* **line** *{string}*

#### return
* *{pyplus.data.DataObjectMixin}*

### to_dict(self)
Serialize object to a dict.

#### return
* *{pyplus.json.Object}*

### to_line(self)
Serialize object to a line of text, needs to be overridden to be used.

#### return
* *{string}*

### to_list(self)
Serialize object to a list.

#### return
* *{pyplus.json.Array}*

## DataObjectsMixin(iterable=None)
A mixin to create a container of data driven objects that can be easily serialized and deserialized.
If used as super class, subclass must override '\_\_CLASS\_\_' attribute with a subclass of DataObjectMixin.

### from_table(path, delimiter=',', headers=True, parse=True)
Deserialize object from a text delimited table, e.g. csv.

#### arguments
* **path** *{string or pathlib.Path}*
* **delimiter** *{string}*
* **headers** *{bool}*: Does the table contain headers.
* **parse** *{bool or function}*: Should strings be parsed (if bool) or parser (if function).

#### return
* *{pyplus.data.DataObjectsMixin}*

### from_txt_file(path)
Deserialize object from a text file, from_line of '\_\_CLASS\_\_' needs to be overridden.

#### arguments
* **path** *{sting or pathlib.Path}*

#### return
* *{pyplus.data.DataObjectsMixin}*

### to_table(self, path, delimiter=',', headers=True)
Serialize object to a text delimited table, e.g. csv.

#### arguments
* **path** *{string or pathlib.Path}*
* **delimiter** *{string}*
* **headers** *{bool}*: Write table headers.

### to_txt_file(self, path)
Serialize object to a text file, to_line of '\_\_CLASS\_\_' needs to be overridden.

#### arguments
* **path** *{sting or pathlib.Path}*

## dataobject(*headers)
Class decorator to mixin DataObjectMixin to class.

#### arguments
* **headers** *{string[]}*: list of strings that represent an ordered dict key to '\_\_init\_\_' arg mapping.

#### return
* *{function}*: decorator that will create a subclass of the decorated class and DataObjectMixin

## dataobjects(data_object_class)
Class decorator to mixin DataObjectsMixin to class.

#### arguments
* **data_object_class** *{type}*: Subclass of DataObjectMixin.

#### return
* *{function}*: decorator that will create a subclass of the decorated class and DataObjectsMixin

