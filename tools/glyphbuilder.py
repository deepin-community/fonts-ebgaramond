import os
import sys
import importlib
import fontforge


#def componentsByFontname(font, fontname):
#    module_name = fontname + "_components"
#    module = __import__(module_name)

def composeAccented(glyph, glyphComponents):
    """Compose accented glyphs.
    
    Get the components from the dictionary and build the new glyph
    from them."""
    
    glif = glyph

    components = glyphComponents[glif.glyphname]
 
    base = components[0]
    marks = components[1:]
    
    greekUC = ['Alpha', 'Epsilon', 'Eta', 'Iota', 'Omicron', 'Rho', 'Upsilon', 'uni03A9']

    glif.clear()
    glif.addReference(base)

    glif.useRefsMetrics(base)

    for mark in marks:
        glif.appendAccent(mark)

    l = glif.left_side_bearing
    
    if base in greekUC:
        if l < -19:
            glif.useRefsMetrics(base, False)
            glif.left_side_bearing = -20
        else:
            glif.useRefsMetrics(base, True)
        
    elif base == 'space.stack':
            glif.useRefsMetrics(base, False)
            glif.left_side_bearing = 30
            glif.right_side_bearing = 30
    else:
        glif.useRefsMetrics(base, True)

def buildAccentedGlyphs(junk,object):
#    """Get the names of the selected glyphs in a font.
#    
#    Call the composing function for every glyph that has an entry 
#    in the dictionary."""
#    componentsByFontname(font, font.fontname)

    font = object if type(object).__name__ == "font" else object.font
    font_file = os.path.normpath(font.path)
    top_level = os.path.split(os.path.split(font_file)[0])[0]
    tool_path = os.path.join(top_level, "tools")
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    import_successful = True
    try:
        glyphcomponents = importlib.import_module("glyphcomponents")
    except:
        import_successful = False
        fontforge.postError("Cannot import Python module glyphcomponents",
                            "This script is made to work with the SFDs residing in top_level/SFD and the module in top_level/tools.")

    if import_successful:
        try:  
            reload(glyphcomponents)
            glyphComponents = glyphcomponents.glyphComponents

            if type(object).__name__ == "font":
                for glyph in object.selection.byGlyphs:
                    if glyph.glyphname in glyphComponents.keys():
                        composeAccented(glyph, glyphComponents)
                    else:
                        continue
            else:
                if object.glyphname in glyphComponents.keys():
                    composeAccented(object, glyphComponents)
                else:
                    logWarning('This glyph has no entry in the dictionary')

        except BaseException as e:
          fontforge.postError("Building glyphs failed", str(e))

fontforge.registerMenuItem(buildAccentedGlyphs,None,None,("Font","Glyph"),None,"Glyphbuilder");
