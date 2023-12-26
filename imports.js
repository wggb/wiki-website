import "tinymce/tinymce";

import "tinymce/icons/default/icons";
import "tinymce/models/dom/model";
import "tinymce/themes/silver/theme";

import "tinymce/plugins/advlist";
import "tinymce/plugins/code/plugin";
import "tinymce/plugins/emoticons";
import "tinymce/plugins/emoticons/js/emojis";
import "tinymce/plugins/help/plugin";
import "tinymce/plugins/link/plugin";
import "tinymce/plugins/lists/plugin";
import "tinymce/plugins/table/plugin";

// import "tinymce/plugins/image/plugin";

import contentCss from "tinymce/skins/content/dark/content.css";
import contentUiCss from "tinymce/skins/ui/oxide-dark/content.css";

export function tinymce_init(selector) {
  tinymce.init({
    selector: selector,
    plugins: "advlist code emoticons link lists table",
    toolbar: "bold italic | bullist numlist | link emoticons",
    skin: false,
    content_css: false,
    promotion: false,
    branding: false,
    menubar: false,
    statusbar: false,
    content_style: `${contentUiCss.toString()}\n${contentCss.toString()}\nbody{background-color:hsl(231 15% 18%);}`,
  });
}
