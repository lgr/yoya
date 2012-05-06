(function(a){function d(){if(!a.fn.ajaxSubmit.debug)return;var b="[jquery.form] "+Array.prototype.join.call(arguments,"");if(window.console&&window.console.log){window.console.log(b)}else if(window.opera&&window.opera.postError){window.opera.postError(b)}}function c(b){var c=b.target;var d=a(c);if(!d.is(":submit,input:image")){var e=d.closest(":submit");if(e.length==0){return}c=e[0]}var f=this;f.clk=c;if(c.type=="image"){if(b.offsetX!=undefined){f.clk_x=b.offsetX;f.clk_y=b.offsetY}else if(typeof a.fn.offset=="function"){var g=d.offset();f.clk_x=b.pageX-g.left;f.clk_y=b.pageY-g.top}else{f.clk_x=b.pageX-c.offsetLeft;f.clk_y=b.pageY-c.offsetTop}}setTimeout(function(){f.clk=f.clk_x=f.clk_y=null},100)}function b(b){var c=b.data;if(!b.isDefaultPrevented()){b.preventDefault();a(this).ajaxSubmit(c)}}a.fn.ajaxSubmit=function(b){function x(e){function E(b){if(o.aborted||D){return}try{B=w(n)}catch(c){d("cannot access response document: ",c);b=v}if(b===u&&o){o.abort("timeout");return}else if(b==v&&o){o.abort("server abort");return}if(!B||B.location.href==j.iframeSrc){if(!r)return}n.detachEvent?n.detachEvent("onload",E):n.removeEventListener("load",E,false);var e="success",f;try{if(r){throw"timeout"}var g=j.dataType=="xml"||B.XMLDocument||a.isXMLDoc(B);d("isXml="+g);if(!g&&window.opera&&(B.body==null||B.body.innerHTML=="")){if(--C){d("requeing onLoad callback, DOM not available");setTimeout(E,250);return}}var h=B.body?B.body:B.documentElement;o.responseText=h?h.innerHTML:null;o.responseXML=B.XMLDocument?B.XMLDocument:B;if(g)j.dataType="xml";o.getResponseHeader=function(a){var b={"content-type":j.dataType};return b[a]};if(h){o.status=Number(h.getAttribute("status"))||o.status;o.statusText=h.getAttribute("statusText")||o.statusText}var i=(j.dataType||"").toLowerCase();var l=/(json|script|text)/.test(i);if(l||j.textarea){var p=B.getElementsByTagName("textarea")[0];if(p){o.responseText=p.value;o.status=Number(p.getAttribute("status"))||o.status;o.statusText=p.getAttribute("statusText")||o.statusText}else if(l){var q=B.getElementsByTagName("pre")[0];var t=B.getElementsByTagName("body")[0];if(q){o.responseText=q.textContent?q.textContent:q.innerText}else if(t){o.responseText=t.textContent?t.textContent:t.innerText}}}else if(i=="xml"&&!o.responseXML&&o.responseText!=null){o.responseXML=F(o.responseText)}try{A=H(o,i,j)}catch(b){e="parsererror";o.error=f=b||e}}catch(b){d("error caught: ",b);e="error";o.error=f=b||e}if(o.aborted){d("upload aborted");e=null}if(o.status){e=o.status>=200&&o.status<300||o.status===304?"success":"error"}if(e==="success"){j.success&&j.success.call(j.context,A,"success",o);k&&a.event.trigger("ajaxSuccess",[o,j])}else if(e){if(f==undefined)f=o.statusText;j.error&&j.error.call(j.context,o,e,f);k&&a.event.trigger("ajaxError",[o,j,f])}k&&a.event.trigger("ajaxComplete",[o,j]);if(k&&!--a.active){a.event.trigger("ajaxStop")}j.complete&&j.complete.call(j.context,o,e);D=true;if(j.timeout)clearTimeout(s);setTimeout(function(){if(!j.iframeTarget)m.remove();o.responseXML=null},100)}function z(){function h(){try{var a=w(n).readyState;d("state = "+a);if(a.toLowerCase()=="uninitialized")setTimeout(h,50)}catch(b){d("Server abort: ",b," (",b.name,")");E(v);s&&clearTimeout(s);s=undefined}}var b=g.attr("target"),e=g.attr("action");f.setAttribute("target",l);if(!c){f.setAttribute("method","POST")}if(e!=j.url){f.setAttribute("action",j.url)}if(!j.skipEncodingOverride&&(!c||/post/i.test(c))){g.attr({encoding:"multipart/form-data",enctype:"multipart/form-data"})}if(j.timeout){s=setTimeout(function(){r=true;E(u)},j.timeout)}var i=[];try{if(j.extraData){for(var k in j.extraData){i.push(a('<input type="hidden" name="'+k+'">').attr("value",j.extraData[k]).appendTo(f)[0])}}if(!j.iframeTarget){m.appendTo("body");n.attachEvent?n.attachEvent("onload",E):n.addEventListener("load",E,false)}setTimeout(h,15);f.submit()}finally{f.setAttribute("action",e);if(b){f.setAttribute("target",b)}else{g.removeAttr("target")}a(i).remove()}}function w(a){var b=a.contentWindow?a.contentWindow.document:a.contentDocument?a.contentDocument:a.document;return b}var f=g[0],h,i,j,k,l,m,n,o,p,q,r,s;var t=!!a.fn.prop;if(e){if(t){for(i=0;i<e.length;i++){h=a(f[e[i].name]);h.prop("disabled",false)}}else{for(i=0;i<e.length;i++){h=a(f[e[i].name]);h.removeAttr("disabled")}}}if(a(":input[name=submit],:input[id=submit]",f).length){alert('Error: Form elements must not have name or id of "submit".');return}j=a.extend(true,{},a.ajaxSettings,b);j.context=j.context||j;l="jqFormIO"+(new Date).getTime();if(j.iframeTarget){m=a(j.iframeTarget);q=m.attr("name");if(q==null)m.attr("name",l);else l=q}else{m=a('<iframe name="'+l+'" src="'+j.iframeSrc+'" />');m.css({position:"absolute",top:"-1000px",left:"-1000px"})}n=m[0];o={aborted:0,responseText:null,responseXML:null,status:0,statusText:"n/a",getAllResponseHeaders:function(){},getResponseHeader:function(){},setRequestHeader:function(){},abort:function(b){var c=b==="timeout"?"timeout":"aborted";d("aborting upload... "+c);this.aborted=1;m.attr("src",j.iframeSrc);o.error=c;j.error&&j.error.call(j.context,o,c,b);k&&a.event.trigger("ajaxError",[o,j,c]);j.complete&&j.complete.call(j.context,o,c)}};k=j.global;if(k&&!(a.active++)){a.event.trigger("ajaxStart")}if(k){a.event.trigger("ajaxSend",[o,j])}if(j.beforeSend&&j.beforeSend.call(j.context,o,j)===false){if(j.global){a.active--}return}if(o.aborted){return}p=f.clk;if(p){q=p.name;if(q&&!p.disabled){j.extraData=j.extraData||{};j.extraData[q]=p.value;if(p.type=="image"){j.extraData[q+".x"]=f.clk_x;j.extraData[q+".y"]=f.clk_y}}}var u=1;var v=2;var x=a("meta[name=csrf-token]").attr("content");var y=a("meta[name=csrf-param]").attr("content");if(y&&x){j.extraData=j.extraData||{};j.extraData[y]=x}if(j.forceSync){z()}else{setTimeout(z,10)}var A,B,C=50,D;var F=a.parseXML||function(a,b){if(window.ActiveXObject){b=new ActiveXObject("Microsoft.XMLDOM");b.async="false";b.loadXML(a)}else{b=(new DOMParser).parseFromString(a,"text/xml")}return b&&b.documentElement&&b.documentElement.nodeName!="parsererror"?b:null};var G=a.parseJSON||function(a){return window["eval"]("("+a+")")};var H=function(b,c,d){var e=b.getResponseHeader("content-type")||"",f=c==="xml"||!c&&e.indexOf("xml")>=0,g=f?b.responseXML:b.responseText;if(f&&g.documentElement.nodeName==="parsererror"){a.error&&a.error("parsererror")}if(d&&d.dataFilter){g=d.dataFilter(g,c)}if(typeof g==="string"){if(c==="json"||!c&&e.indexOf("json")>=0){g=G(g)}else if(c==="script"||!c&&e.indexOf("javascript")>=0){a.globalEval(g)}}return g}}function w(c){var d=new FormData;for(var e=0;e<c.length;e++){if(c[e].type=="file")continue;d.append(c[e].name,c[e].value)}g.find("input:file:enabled").each(function(){var b=a(this).attr("name"),c=this.files;if(b){for(var e=0;e<c.length;e++)d.append(b,c[e])}});if(b.extraData){for(var f in b.extraData)d.append(f,b.extraData[f])}b.data=null;var h=a.extend(true,{},a.ajaxSettings,b,{contentType:false,processData:false,cache:false,type:"POST"});h.data=null;var i=h.beforeSend;h.beforeSend=function(a,c){c.data=d;if(a.upload){a.upload.onprogress=function(a){c.progress(a.position,a.total)}}if(i)i.call(c,a,b)};a.ajax(h)}if(!this.length){d("ajaxSubmit: skipping submit process - no element selected");return this}var c,e,f,g=this;if(typeof b=="function"){b={success:b}}c=this.attr("method");e=this.attr("action");f=typeof e==="string"?a.trim(e):"";f=f||window.location.href||"";if(f){f=(f.match(/^([^#]+)/)||[])[1]}b=a.extend(true,{url:f,success:a.ajaxSettings.success,type:c||"GET",iframeSrc:/^https/i.test(window.location.href||"")?"javascript:false":"about:blank"},b);var h={};this.trigger("form-pre-serialize",[this,b,h]);if(h.veto){d("ajaxSubmit: submit vetoed via form-pre-serialize trigger");return this}if(b.beforeSerialize&&b.beforeSerialize(this,b)===false){d("ajaxSubmit: submit aborted via beforeSerialize callback");return this}var i=b.traditional;if(i===undefined){i=a.ajaxSettings.traditional}var j,k,l,m=this.formToArray(b.semantic);if(b.data){b.extraData=b.data;j=a.param(b.data,i)}if(b.beforeSubmit&&b.beforeSubmit(m,this,b)===false){d("ajaxSubmit: submit aborted via beforeSubmit callback");return this}this.trigger("form-submit-validate",[m,this,b,h]);if(h.veto){d("ajaxSubmit: submit vetoed via form-submit-validate trigger");return this}var n=a.param(m,i);if(j){n=n?n+"&"+j:j}if(b.type.toUpperCase()=="GET"){b.url+=(b.url.indexOf("?")>=0?"&":"?")+n;b.data=null}else{b.data=n}var o=[];if(b.resetForm){o.push(function(){g.resetForm()})}if(b.clearForm){o.push(function(){g.clearForm(b.includeHidden)})}if(!b.dataType&&b.target){var p=b.success||function(){};o.push(function(c){var d=b.replaceTarget?"replaceWith":"html";a(b.target)[d](c).each(p,arguments)})}else if(b.success){o.push(b.success)}b.success=function(a,c,d){var e=b.context||b;for(var f=0,h=o.length;f<h;f++){o[f].apply(e,[a,c,d||g,g])}};var q=a("input:file:enabled[value]",this);var r=q.length>0;var s="multipart/form-data";var t=g.attr("enctype")==s||g.attr("encoding")==s;var u=!!(r&&q.get(0).files&&window.FormData);d("fileAPI :"+u);var v=(r||t)&&!u;if(b.iframe!==false&&(b.iframe||v)){if(b.closeKeepAlive){a.get(b.closeKeepAlive,function(){x(m)})}else{x(m)}}else if((r||t)&&u){b.progress=b.progress||a.noop;w(m)}else{a.ajax(b)}this.trigger("form-submit-notify",[this,b]);return this};a.fn.ajaxForm=function(e){e=e||{};e.delegation=e.delegation&&a.isFunction(a.fn.on);if(!e.delegation&&this.length===0){var f={s:this.selector,c:this.context};if(!a.isReady&&f.s){d("DOM not ready, queuing ajaxForm");a(function(){a(f.s,f.c).ajaxForm(e)});return this}d("terminating; zero elements found by selector"+(a.isReady?"":" (DOM not ready)"));return this}if(e.delegation){a(document).off("submit.form-plugin",this.selector,b).off("click.form-plugin",this.selector,c).on("submit.form-plugin",this.selector,e,b).on("click.form-plugin",this.selector,e,c);return this}return this.ajaxFormUnbind().bind("submit.form-plugin",e,b).bind("click.form-plugin",e,c)};a.fn.ajaxFormUnbind=function(){return this.unbind("submit.form-plugin click.form-plugin")};a.fn.formToArray=function(b){var c=[];if(this.length===0){return c}var d=this[0];var e=b?d.getElementsByTagName("*"):d.elements;if(!e){return c}var f,g,h,i,j,k,l;for(f=0,k=e.length;f<k;f++){j=e[f];h=j.name;if(!h){continue}if(b&&d.clk&&j.type=="image"){if(!j.disabled&&d.clk==j){c.push({name:h,value:a(j).val(),type:j.type});c.push({name:h+".x",value:d.clk_x},{name:h+".y",value:d.clk_y})}continue}i=a.fieldValue(j,true);if(i&&i.constructor==Array){for(g=0,l=i.length;g<l;g++){c.push({name:h,value:i[g]})}}else if(i!==null&&typeof i!="undefined"){c.push({name:h,value:i,type:j.type})}}if(!b&&d.clk){var m=a(d.clk),n=m[0];h=n.name;if(h&&!n.disabled&&n.type=="image"){c.push({name:h,value:m.val()});c.push({name:h+".x",value:d.clk_x},{name:h+".y",value:d.clk_y})}}return c};a.fn.formSerialize=function(b){return a.param(this.formToArray(b))};a.fn.fieldSerialize=function(b){var c=[];this.each(function(){var d=this.name;if(!d){return}var e=a.fieldValue(this,b);if(e&&e.constructor==Array){for(var f=0,g=e.length;f<g;f++){c.push({name:d,value:e[f]})}}else if(e!==null&&typeof e!="undefined"){c.push({name:this.name,value:e})}});return a.param(c)};a.fn.fieldValue=function(b){for(var c=[],d=0,e=this.length;d<e;d++){var f=this[d];var g=a.fieldValue(f,b);if(g===null||typeof g=="undefined"||g.constructor==Array&&!g.length){continue}g.constructor==Array?a.merge(c,g):c.push(g)}return c};a.fieldValue=function(b,c){var d=b.name,e=b.type,f=b.tagName.toLowerCase();if(c===undefined){c=true}if(c&&(!d||b.disabled||e=="reset"||e=="button"||(e=="checkbox"||e=="radio")&&!b.checked||(e=="submit"||e=="image")&&b.form&&b.form.clk!=b||f=="select"&&b.selectedIndex==-1)){return null}if(f=="select"){var g=b.selectedIndex;if(g<0){return null}var h=[],i=b.options;var j=e=="select-one";var k=j?g+1:i.length;for(var l=j?g:0;l<k;l++){var m=i[l];if(m.selected){var n=m.value;if(!n){n=m.attributes&&m.attributes["value"]&&!m.attributes["value"].specified?m.text:m.value}if(j){return n}h.push(n)}}return h}return a(b).val()};a.fn.clearForm=function(b){return this.each(function(){a("input,select,textarea",this).clearFields(b)})};a.fn.clearFields=a.fn.clearInputs=function(a){var b=/^(?:color|date|datetime|email|month|number|password|range|search|tel|text|time|url|week)$/i;return this.each(function(){var c=this.type,d=this.tagName.toLowerCase();if(b.test(c)||d=="textarea"||a&&/hidden/.test(c)){this.value=""}else if(c=="checkbox"||c=="radio"){this.checked=false}else if(d=="select"){this.selectedIndex=-1}})};a.fn.resetForm=function(){return this.each(function(){if(typeof this.reset=="function"||typeof this.reset=="object"&&!this.reset.nodeType){this.reset()}})};a.fn.enable=function(a){if(a===undefined){a=true}return this.each(function(){this.disabled=!a})};a.fn.selected=function(b){if(b===undefined){b=true}return this.each(function(){var c=this.type;if(c=="checkbox"||c=="radio"){this.checked=b}else if(this.tagName.toLowerCase()=="option"){var d=a(this).parent("select");if(b&&d[0]&&d[0].type=="select-one"){d.find("option").selected(false)}this.selected=b}})};a.fn.ajaxSubmit.debug=false;})(jQuery)