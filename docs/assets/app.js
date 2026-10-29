(function(){var q=document.getElementById('q');if(!q)return;var c=document.getElementById('cat'),r=document.getElementById('reg'),n=document.getElementById('cnt');
var rows=[].slice.call(document.querySelectorAll('table.tools tbody tr'));
function f(){var s=q.value.trim().toLowerCase(),k=0;rows.forEach(function(t){var ok=(!s||t.dataset.q.indexOf(s)>-1)&&(!c.value||t.dataset.cat===c.value)&&(!r.value||t.dataset.region===r.value);t.hidden=!ok;if(ok)k++});n.textContent=k+' von '+rows.length+' Tools';}
[q,c,r].forEach(function(x){x.addEventListener('input',f)});f();})();
