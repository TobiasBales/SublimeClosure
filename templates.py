import string

require = string.Template("goog.require('$namespace');")

provide = string.Template("goog.provide('$namespace');")

prototype_property = string.Template("""/**
 * @type {${3:[type]}}
 */
$namespace.prototype.${1:[name]} = ${2:[value]};""")

prototype_function = string.Template("""/**
 * ${4}
 */
$namespace.prototype.${1:[name]} = function(${2:[params]}) {
    ${3}
};""")

static_property = string.Template("""/**
 * @type {${3:[type]}}
 */
$namespace.${1:[name]} = ${2:[value]};""")

static_function = string.Template("""/**
 * ${4}
 */
$namespace.${1:[name]} = function(${2:[params]}) {
    ${3}
};""")

static_accessor = string.Template("$namespace.${1:[property]}")


enumeration = string.Template("""/**
 * @enum {${2:[type]}}
 */
$namespace.${1:[name]} = {
    ${3:[values]}
};""")

component = string.Template("""


/**
 * @constructor
 * @extends {goog.ui.Component}
 */
$namespace = function() {
    goog.base(this);
};
goog.inherits($namespace, goog.ui.Component);


/**
 * @inheritDoc
 */
$namespace.prototype.createDom = function() {
    goog.base(this, 'createDom');

    var dom = this.getDomHelper();
    var elem = this.getElement();
};


/**
 * @inheritDoc
 */
$namespace.prototype.enterDocument = function() {
    goog.base(this, 'enterDocument');

    var handler = this.getHandler();
};


/**
 * @inheritDoc
 */
$namespace.prototype.disposeInternal = function() {
    goog.base(this, 'disposeInternal');
};""")


control = string.Template("""


/**
 * @constructor
 * @extends {goog.ui.Control}
 * @param {goog.ui.ControlContent} content
 */
$namespace = function(content) {
    goog.base(this, content);
};
goog.inherits($namespace, goog.ui.Control);


/**
 * @inheritDoc
 */
$namespace.prototype.enterDocument = function() {
    goog.base(this, 'enterDocument');

    var handler = this.getHandler();
};


/**
 * @inheritDoc
 */
$namespace.prototype.disposeInternal = function() {
    goog.base(this, 'disposeInternal');
};""")


control_renderer = string.Template("""


/**
 * @constructor
 * @extends {goog.ui.ControlRenderer}
 */
$namespace = function() {
    goog.base(this);
};
goog.inherits($namespace, goog.ui.Control);
goog.addSingletonGetter($namespace);


/**
 * @inheritDoc
 */
$namespace.prototype.createDom = function(control) {
    return goog.base(this, 'createDom', control);
};""")
