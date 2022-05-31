/*
 Highcharts JS v9.1.1 (2021-06-03)

 Module for adding patterns and images as point fills.

 (c) 2010-2021 Highsoft AS
 Author: Torstein Hnsi, ystein Moseng

 License: www.highcharts.com/license
*/
'use strict';(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/pattern-fill",["highcharts"],function(e){b(e);b.Highcharts=e;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function e(b,e,r,p){b.hasOwnProperty(e)||(b[e]=p.apply(null,r))}b=b?b._modules:{};e(b,"Extensions/PatternFill.js",[b["Core/Animation/AnimationUtilities.js"],b["Core/Chart/Chart.js"],b["Core/Globals.js"],
b["Core/DefaultOptions.js"],b["Core/Series/Point.js"],b["Core/Series/Series.js"],b["Core/Renderer/SVG/SVGRenderer.js"],b["Core/Utilities.js"]],function(b,e,r,p,t,u,v,l){function w(a,c){a=JSON.stringify(a);var b=a.length||0,f=0,d=0;if(c){c=Math.max(Math.floor(b/500),1);for(var n=0;n<b;n+=c)f+=a.charCodeAt(n);f&=f}for(;d<b;++d)c=a.charCodeAt(d),f=(f<<5)-f+c,f&=f;return f.toString(16).replace("-","1")}var z=b.animObject,A=p.getOptions;b=l.addEvent;var B=l.erase,x=l.merge,q=l.pick,C=l.removeEvent;p=l.wrap;
var y=r.patterns=function(){var a=[],c=A().colors;"M 0 0 L 10 10 M 9 -1 L 11 1 M -1 9 L 1 11;M 0 10 L 10 0 M -1 1 L 1 -1 M 9 11 L 11 9;M 3 0 L 3 10 M 8 0 L 8 10;M 0 3 L 10 3 M 0 8 L 10 8;M 0 3 L 5 3 L 5 0 M 5 10 L 5 7 L 10 7;M 3 3 L 8 3 L 8 8 L 3 8 Z;M 5 5 m -4 0 a 4 4 0 1 1 8 0 a 4 4 0 1 1 -8 0;M 10 3 L 5 3 L 5 0 M 5 10 L 5 7 L 0 7;M 2 5 L 5 2 L 8 5 L 5 8 Z;M 0 0 L 5 10 L 10 0".split(";").forEach(function(b,f){a.push({path:b,color:c[f],width:10,height:10})});return a}();t.prototype.calculatePatternDimensions=
function(a){if(!a.width||!a.height){var c=this.graphic&&(this.graphic.getBBox&&this.graphic.getBBox(!0)||this.graphic.element&&this.graphic.element.getBBox())||{},b=this.shapeArgs;b&&(c.width=b.width||c.width,c.height=b.height||c.height,c.x=b.x||c.x,c.y=b.y||c.y);if(a.image){if(!c.width||!c.height){a._width="defer";a._height="defer";return}a.aspectRatio&&(c.aspectRatio=c.width/c.height,a.aspectRatio>c.aspectRatio?c.aspectWidth=c.height*a.aspectRatio:c.aspectHeight=c.width/a.aspectRatio);a._width=
a.width||Math.ceil(c.aspectWidth||c.width);a._height=a.height||Math.ceil(c.aspectHeight||c.height)}a.width||(a._x=a.x||0,a._x+=c.x-Math.round(c.aspectWidth?Math.abs(c.aspectWidth-c.width)/2:0));a.height||(a._y=a.y||0,a._y+=c.y-Math.round(c.aspectHeight?Math.abs(c.aspectHeight-c.height)/2:0))}};v.prototype.addPattern=function(a,c){c=q(c,!0);var b=z(c),f=a.width||a._width||32,d=a.height||a._height||32,n=a.color||"#343434",g=a.id,e=this,m=function(a){e.rect(0,0,f,d).attr({fill:a}).add(k)};g||(this.idCounter=
this.idCounter||0,g="highcharts-pattern-"+this.idCounter+"-"+(this.chartIndex||0),++this.idCounter);this.forExport&&(g+="-export");this.defIds=this.defIds||[];if(!(-1<this.defIds.indexOf(g))){this.defIds.push(g);var h={id:g,patternUnits:"userSpaceOnUse",patternContentUnits:a.patternContentUnits||"userSpaceOnUse",width:f,height:d,x:a._x||a.x||0,y:a._y||a.y||0};a.patternTransform&&(h.patternTransform=a.patternTransform);var k=this.createElement("pattern").attr(h).add(this.defs);k.id=g;a.path?(h=l.isObject(a.path)?
a.path:{d:a.path},a.backgroundColor&&m(a.backgroundColor),m={d:h.d},this.styledMode||(m.stroke=h.stroke||n,m["stroke-width"]=q(h.strokeWidth,2),m.fill=h.fill||"none"),h.transform&&(m.transform=h.transform),this.createElement("path").attr(m).add(k),k.color=n):a.image&&(c?this.image(a.image,0,0,f,d,function(){this.animate({opacity:q(a.opacity,1)},b);C(this.element,"load")}).attr({opacity:0}).add(k):this.image(a.image,0,0,f,d).add(k));a.image&&c||"undefined"===typeof a.opacity||[].forEach.call(k.element.childNodes,
function(c){c.setAttribute("opacity",a.opacity)});this.patternElements=this.patternElements||{};return this.patternElements[g]=k}};p(u.prototype,"getColor",function(a){var c=this.options.color;c&&c.pattern&&!c.pattern.color?(delete this.options.color,a.apply(this,Array.prototype.slice.call(arguments,1)),c.pattern.color=this.color,this.color=this.options.color=c):a.apply(this,Array.prototype.slice.call(arguments,1))});b(u,"render",function(){var a=this.chart.isResizing;(this.isDirtyData||a||!this.chart.hasRendered)&&
(this.points||[]).forEach(function(c){var b=c.options&&c.options.color;b&&b.pattern&&(!a||c.shapeArgs&&c.shapeArgs.width&&c.shapeArgs.height?c.calculatePatternDimensions(b.pattern):(b.pattern._width="defer",b.pattern._height="defer"))})});b(t,"afterInit",function(){var a=this.options.color;a&&a.pattern&&("string"===typeof a.pattern.path&&(a.pattern.path={d:a.pattern.path}),this.color=this.options.color=x(this.series.options.color,a))});b(v,"complexColor",function(a){var c=a.args[0],b=a.args[1];a=
a.args[2];var f=this.chartIndex||0,d=c.pattern,e="#343434";"undefined"!==typeof c.patternIndex&&y&&(d=y[c.patternIndex]);if(!d)return!0;if(d.image||"string"===typeof d.path||d.path&&d.path.d){var g=a.parentNode&&a.parentNode.getAttribute("class");g=g&&-1<g.indexOf("highcharts-legend");"defer"!==d._width&&"defer"!==d._height||t.prototype.calculatePatternDimensions.call({graphic:{element:a}},d);if(g||!d.id)d=x({},d),d.id="highcharts-pattern-"+f+"-"+w(d)+w(d,!0);this.addPattern(d,!this.forExport&&q(d.animation,
this.globalAnimation,{duration:100}));e="url("+this.url+"#"+(d.id+(this.forExport?"-export":""))+")"}else e=d.color||e;a.setAttribute(b,e);c.toString=function(){return e};return!1});b(e,"endResize",function(){(this.renderer&&this.renderer.defIds||[]).filter(function(a){return a&&a.indexOf&&0===a.indexOf("highcharts-pattern-")}).length&&(this.series.forEach(function(a){a.points.forEach(function(a){(a=a.options&&a.options.color)&&a.pattern&&(a.pattern._width="defer",a.pattern._height="defer")})}),this.redraw(!1))});
b(e,"redraw",function(){var a={},c=this.renderer,b=(c.defIds||[]).filter(function(a){return a.indexOf&&0===a.indexOf("highcharts-pattern-")});b.length&&([].forEach.call(this.renderTo.querySelectorAll('[color^="url("], [fill^="url("], [stroke^="url("]'),function(b){if(b=b.getAttribute("fill")||b.getAttribute("color")||b.getAttribute("stroke"))b=b.replace(c.url,"").replace("url(#","").replace(")",""),a[b]=!0}),b.forEach(function(b){a[b]||(B(c.defIds,b),c.patternElements[b]&&(c.patternElements[b].destroy(),
delete c.patternElements[b]))}))});""});e(b,"masters/modules/pattern-fill.src.js",[],function(){})});
//# sourceMappingURL=pattern-fill.js.map