import{d as k,_ as $,o as n,c as t,e,t as l,F as _,i as S,j as r,u as I,k as j,l as D,r as V,h as i,m as L,v as N,n as B,p as F,g as T}from"./index-25e6ba79.js";import{a as b}from"./config-9d7f0f6c.js";const M=k({props:{submission:{type:Object,required:!0}}}),U={class:"mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 m-4"},q={class:"p-2"},E={class:"font-semibold"};function O(s,o,v,g,c,m){return n(),t("div",U,[e("div",q,[e("div",null," Submitted by "+l(s.submission.user_name),1),e("div",null," on "+l(s.submission.formatted_date)+" at "+l(s.submission.formatted_time),1)]),(n(!0),t(_,null,S(s.submission.fields,d=>(n(),t("div",{key:d.id,class:"p-2"},[e("div",E,l(d.title),1),e("div",null,l(d.value),1)]))),128))])}const R=$(M,[["render",O]]),X=k({components:{SubmissionCard:R},setup(){const s=r("forminder"),o=r(!0),v=r("csv"),g=r([]),c=r(1),m=r(10),d=r(1),h=I().query.formId,y=r(),C=()=>{const u=v.value==="csv"?b+"/api/v1/submissions/export/csv?formId="+h:b+"/api/v1/submissions/export/xlsx?formId="+h;window.location.href=u},w=async()=>{const u=await fetch(b+`/api/v1/submissions?formId=${h}&page=${c.value}&per_page=${m.value}`);if(o.value=!1,u.status===401){D();return}if(u.ok){const f=await u.json();y.value=f.form_name,g.value=f.submissions,d.value=Math.floor(f.total/m.value)+(f.total%m.value>0?1:0)}},P=u=>{c.value=u,w()};return j(()=>{w()}),{loading:o,formName:y,slashCommand:s,exportType:v,submissions:g,downloadData:C,page:c,lastPage:d,changePage:P}}});const p=s=>(F("data-v-14b4445e"),s=s(),T(),s),z={key:0,class:"w-full text-3xl text-center p-5"},A={class:"text-3xl"},G={key:1,class:"loading-indicator"},H={class:"flex justify-around"},J={key:0},K=p(()=>e("span",null," Export as ",-1)),Q=p(()=>e("option",{value:"csv"},"CSV",-1)),W=p(()=>e("option",{value:"xlsx"},"XLSX",-1)),Y=[Q,W],Z={class:"flex flex-wrap justify-center place-content-evenly"},x={key:0,class:"mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4"},ss=p(()=>e("div",{class:"p-1"}," There are no submissions for this form. ",-1)),es=p(()=>e("div",{class:"p-1"}," Schedule the form in slack by running: ",-1)),os={class:"p-1 code"},ns=p(()=>e("div",{class:"p-1"},' and then pressing "Schedule". ',-1)),ts=p(()=>e("div",{class:"p-1"},' Or fill it without scheduling by pressing "Fill now". ',-1)),as={key:0,class:"flex justify-center"},is={class:"m-3"},ls={class:"p-3"};function ds(s,o,v,g,c,m){const d=V("SubmissionCard");return n(),t(_,null,[s.loading?i("",!0):(n(),t("div",z,[e("span",A,l(s.formName)+" - Submissions",1)])),s.loading?(n(),t("div",G," Loading... ")):i("",!0),e("div",null,[e("div",H,[s.loading?i("",!0):(n(),t("div",J,[K,L(e("select",{name:"export",id:"export",class:"p-2 m-1 rounded-md shadow","onUpdate:modelValue":o[0]||(o[0]=a=>s.exportType=a)},Y,512),[[N,s.exportType]]),e("button",{id:"download-btn",class:"bg-greenish p-2 m-1 rounded",onClick:o[1]||(o[1]=(...a)=>s.downloadData&&s.downloadData(...a))}," Download ")]))]),e("div",Z,[(n(!0),t(_,null,S(s.submissions,a=>(n(),B(d,{key:a.id,submission:a},null,8,["submission"]))),128)),!s.loading&&!s.submissions.length?(n(),t("div",x,[ss,es,e("div",os," /"+l(s.slashCommand)+" list ",1),ns,ts])):i("",!0)]),s.loading?i("",!0):(n(),t("div",as,[e("div",is,[s.page>1?(n(),t("button",{key:0,onClick:o[2]||(o[2]=a=>s.changePage(1)),class:"p-3 underline"}," First ")):i("",!0),s.page>1?(n(),t("button",{key:1,onClick:o[3]||(o[3]=a=>s.changePage(s.page-1)),class:"p-3 underline"}," Previous ")):i("",!0),e("span",ls," Page "+l(s.page)+" of "+l(s.lastPage),1),s.page<s.lastPage?(n(),t("button",{key:2,onClick:o[4]||(o[4]=a=>s.changePage(s.page+1)),class:"p-3 underline"}," Next ")):i("",!0),s.page<s.lastPage?(n(),t("button",{key:3,onClick:o[5]||(o[5]=a=>s.changePage(s.lastPage)),class:"p-3 underline"}," Last ")):i("",!0)])]))])],64)}const ps=$(X,[["render",ds],["__scopeId","data-v-14b4445e"]]);export{ps as default};
