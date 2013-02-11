import functools
import sublime
import sublime_plugin
import templates


def render(template, params):
    return template.safe_substitute(params)


class AddClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = "Enter the name of the " + self.type()
        self.view.window().show_input_panel(text, "", functools.partial(self.add, edit), None, None)

    def add(self, edit, name):
        self.add_provide(edit, name)
        self.add_require(edit)
        self.add_template(edit, name)

    def add_provide(self, edit, name):
        if self.has_provide(name):
            return
        self.view.insert(edit, self.provide_position(), render(templates.provide, {'namespace': name}) + "\n")

    def add_require(self, edit):
        name = self.require()
        if self.has_require(name):
            return
        self.view.insert(edit, self.require_position(), render(templates.require, {'namespace': name}) + "\n")

    def add_template(self, edit, name):
        self.view.insert(edit, self.view.size(), render(self.template(), {'namespace': name}))

    def has_provide(self, name):
        return self.view.find("goog.provide\(['\"]" + name + "['\"]\);?", 0) != None

    def has_require(self, name):
        return self.view.find("goog.require\(['\"]" + name + "['\"]\);?", 0) != None

    def last_position_for_pattern(self, pattern):
        regions = self.view.find_all(pattern)
        if (len(regions) == 0):
            return None

        return regions[-1].b

    def provide_position(self):
        position = self.last_position_for_pattern("goog.provide\(['\"](.+)['\"]\);?")
        return position + 1 if position else 0

    def require_position(self):
        position = self.last_position_for_pattern("goog.require\(['\"](.+)['\"]\);?")
        return position + 1 if position else self.provide_position()

    def is_visible(self):
        if (self.view == None):
            return False

        scope = self.view.scope_name(self.view.sel()[0].a)

        #make it work on javascript and new files
        return "source.js" in scope or "text.plain" in scope


class AddComponentCommand(AddClassCommand):
    def type(self):
        return "Component"

    def template(self):
        return templates.component

    def require(self):
        return "goog.ui.Component"


class SublimeClosureListener(sublime_plugin.EventListener):
    def get_provides(self, view):
        namespaces = []
        for provide in view.find_all("goog.provide\(['\"](.+)['\"]\)"):
            namespace = sublime.Region(provide.a + 14, provide.b - 2)
            namespaces.append(view.substr(namespace))
        return namespaces

    def has_multiple_provides(self, view):
        len(self.get_provides(view) > 1)

    def replace_word_with_template(self, view, word, template, params):
        edit = view.begin_edit()
        view.replace(edit, word, "")
        view.run_command("insert_snippet", {"contents": self.render(template, params)})
        view.end_edit(edit)

    def on_query_completions(self, view, prefix, locations):
        namespaces = self.get_provides(view)

        #multi selection was used -> do not add to auto complete
        if (len(locations) != 1):
            return
        location = locations[0]

        scope = view.scope_name(view.sel()[0].a)
        #only autocomplete in javascript and new files
        if not "source.js" in scope or "text.plain" in scope:
            return

        completions = []
        completions.append(("require \t goog.require", render(templates.require, {'namespace': '${1:[namespace]}'})))
        completions.append(("provide \t goog.provide", render(templates.provide, {'namespace': '${1:[namespace]}'})))

        namespace = None
        if (len(namespaces) == 0):
            return completions

        if (len(namespaces) == 1):
            namespace = namespaces[0]
        else:
            regions = []
            for namespace in namespaces:
                regions += view.find_all("^" + namespace)
            regions.sort()
            regions_above = [region for region in regions if region.b < location]
            if (len(regions_above) == 0):
                return completions
            namespace = view.substr(regions_above[-1])

        completions.append(("enumeration",
                            render(templates.enumeration, {'namespace': namespace})))
        completions.append(("prototype property",
                            render(templates.prototype_property, {'namespace': namespace})))
        completions.append(("prototype function",
                            render(templates.prototype_function, {'namespace': namespace})))
        completions.append(("static property",
                            render(templates.static_property, {'namespace': namespace})))
        completions.append(("static function",
                            render(templates.static_function, {'namespace': namespace})))

        return completions
