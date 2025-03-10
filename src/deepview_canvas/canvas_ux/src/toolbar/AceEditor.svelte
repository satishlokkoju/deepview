<!-- MIT License

Copyright (c) 2020 Natesh M Bhat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. -->


<script lang="ts">
    import { createEventDispatcher, tick, onMount, onDestroy } from "svelte";
    import * as ace from "brace";
    import "brace/ext/emmet";
    const dispatch = createEventDispatcher<{
      init: ace.Editor;
      input: string;
      selectionChange: any;
      blur: void;
      changeMode: any;
      commandKey: { err: any; hashId: any; keyCode: any };
      copy: void;
      cursorChange: void;
      cut: void;
      documentChange: { data: any };
      focus: void;
      paste: string;
    }>();
  
    /**
     * translation of vue component to svelte:
     * @link https://github.com/chairuosen/vue2-ace-editor/blob/91051422b36482eaf94271f1a263afa4b998f099/index.js
     **/
    export let value: string = ""; // String, required
    export let lang: string = "json"; // String
    export let theme: string = "chrome"; // String
    export let height: string = "100%"; // null for 100, else integer, used as percent
    export let width: string = "100%"; // null for 100, else integer, used as percent
    export let options: any = {}; // Object
    export let readonly: boolean = false;
    export let keybindings: string = null;
    let editorElement: HTMLElement;
    let editor: ace.Editor;
    let contentBackup: string = "";
  
    const requireEditorPlugins = () => {};
    requireEditorPlugins();
  
    onDestroy(() => {
      if (editor) {
        editor.destroy();
        editor.container.remove();
      }
    });
  
    $: watchValue(value);
    function watchValue(val: string) {
      if (contentBackup !== val && editor && typeof val === "string") {
        editor.session.setValue(val);
        contentBackup = val;
      }
    }
  
    $: watchTheme(theme);
    function watchTheme(newTheme: string) {
      if (editor) {
        editor.setTheme("ace/theme/" + newTheme);
      }
    }
  
    $: watchMode(lang);
    function watchMode(newOption: any) {
      if (editor) {
        editor.getSession().setMode("ace/mode/" + newOption);
      }
    }
  
    $: watchOptions(options);
    function watchOptions(newOption: any) {
      if (editor) {
        editor.setOptions(newOption);
      }
    }
  
    $: watchReadOnlyFlag(readonly);
    function watchReadOnlyFlag(flag) {
      if (editor) {
        editor.setReadOnly(flag);
      }
    }
  
    const resizeOnNextTick = () =>
      tick().then(() => {
        if (editor) {
          editor.resize();
        }
      });
  
    $: if (height !== null && width !== null) {
      resizeOnNextTick();
    }
  
    onMount(() => {
      lang = lang || "text";
      theme = theme || "chrome";
  
      editor = ace.edit(editorElement);
  
      dispatch("init", editor);
      editor.$blockScrolling = Infinity;
      // editor.setOption("enableEmmet", true);
      editor.getSession().setMode("ace/mode/" + lang);
      editor.setTheme("ace/theme/" + theme);
      editor.setValue(value, 1);
      editor.setReadOnly(readonly)
      contentBackup = value;
      setEventCallBacks();
      if (options) {
        editor.setOptions(options);
      }
    });
  
    const ValidPxDigitsRegEx = /^\d*$/;
    function px(n: string): string {
      if (ValidPxDigitsRegEx.test(n)) {
        return n + "px";
      }
      return n;
    }
  
    function setEventCallBacks() {
      editor.onBlur = () => dispatch("blur");
      editor.onChangeMode = (obj) => dispatch("changeMode", obj);
      editor.onCommandKey = (err, hashId, keyCode) =>
        dispatch("commandKey", { err, hashId, keyCode });
      editor.onCopy = () => dispatch("copy");
      editor.onCursorChange = () => dispatch("cursorChange");
      editor.onCut = () => {
        const copyText = editor.getCopyText();
        console.log("cut event : ", copyText);
        editor.insert("");
        dispatch("cut");
      };
      editor.onDocumentChange = (obj: { data: any }) =>
        dispatch("documentChange", obj);
      editor.onFocus = () => dispatch("focus");
      editor.onPaste = (text) => {
        console.log("paste event : ", text);
        editor.insert(text);
        dispatch("paste", text);
      };
      editor.onSelectionChange = (obj) => dispatch("selectionChange", obj);
      editor.on("change", function () {
        const content = editor.getValue();
        value = content;
        dispatch("input", content);
        contentBackup = content;
      });
      
      if (keybindings != null){
        editor.setKeyboardHandler("ace/keyboard/" + keybindings);
      }
    }
  </script>
  
  <div style="width:{px(width)};height:{px(height)}">
    <div bind:this={editorElement} style="width:{px(width)};height:{px(height)}" />
  </div>