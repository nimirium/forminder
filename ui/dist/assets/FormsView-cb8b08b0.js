import{d as m,_ as f,r as y,o as t,c as a,h as n,F as _,i as h,e as s,t as r,b as l,w as d,f as c,p as w,g as v}from"./index-3f89deae.js";const k=m({name:"FormsView",data(){const e=parseInt(this.$route.query.page,10)||1,o=parseInt(this.$route.query.per_page,10)||10;return{loading:!0,forms:[],page:e,per_page:o,total:0,last_page:1,slashCommand:"forminder"}},methods:{async fetchForms(){this.loading=!0;try{const e=await fetch(`/api/v1/forms?page=${this.page}&per_page=${this.per_page}`);if(!e.ok)throw this.loading=!1,new Error("Network response was not ok");const o=await e.json();this.forms=o.forms,this.page=o.page,this.per_page=o.per_page,this.total=o.total,this.loading=!1,this.last_page=Math.floor(this.total/this.per_page)+(this.total%this.per_page>0?1:0)}catch(e){console.error(e),this.loading=!1}}},watch:{$route:{async handler(){this.page=parseInt(this.$route.query.page,10)||1,this.per_page=parseInt(this.$route.query.per_page,10)||10,await this.fetchForms()},immediate:!0}}});const u=e=>(w("data-v-149fff02"),e=e(),v(),e),b=u(()=>s("div",{class:"w-full text-3xl text-center p-5"},[s("span",{class:"text-3xl"},"Forms")],-1)),$={key:0,class:"loading-indicator"},F={key:1,class:"flex flex-wrap justify-center place-content-evenly"},I={class:"font-semibold text-xl p-1"},q={class:"p-1"},C={class:"p-1"},V={class:"list-disc pl-5"},N={class:"font-semibold p-1"},S={class:"bg-greenish rounded-xl p-3 my-2 font-bold shadow-md",style:{color:"#ffffff"}},j={key:0,class:"mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4"},B=u(()=>s("div",{class:"p-1"},"You don't have any forms.",-1)),L=u(()=>s("div",{class:"p-1"},"Create a form in slack by running:",-1)),x={class:"p-1 code"},E={key:2,class:"flex justify-center"},P={class:"m-3"},D={class:"p-3"};function M(e,o,T,Y,z,A){const p=y("router-link");return t(),a("div",null,[b,e.loading?(t(),a("div",$," Loading... ")):n("",!0),e.loading?n("",!0):(t(),a("div",F,[(t(!0),a(_,null,h(e.forms,i=>(t(),a("div",{key:i.id,class:"mygrid-item opacity-75 p-7 rounded-xl shadow-md w-full md:w-1/3 lg:w-1/4 p-4 max-w-lg p-5 m-5"},[s("div",I,r(i.name),1),s("div",q,"Created by "+r(i.user_name),1),s("div",C,[s("ul",V,[(t(!0),a(_,null,h(i.fields,g=>(t(),a("li",{key:g.id},r(g.title),1))),128))])]),s("div",N," Submissions: "+r(i.number_of_submissions),1),s("button",S,[l(p,{to:`/submissions?formId=${i.id}`},{default:d(()=>[c("View submissions")]),_:2},1032,["to"])])]))),128)),!e.loading&&e.forms.length===0?(t(),a("div",j,[B,L,s("div",x,"/"+r(e.slashCommand)+" create",1)])):n("",!0)])),e.loading?n("",!0):(t(),a("div",E,[s("div",P,[e.page>1?(t(),a(_,{key:0},[l(p,{to:{name:"forms",query:{page:1,per_page:e.per_page}},class:"p-3 underline"},{default:d(()=>[c("First ")]),_:1},8,["to"]),l(p,{to:{name:"forms",query:{page:e.page-1,per_page:e.per_page}},class:"p-3 underline"},{default:d(()=>[c("Previous ")]),_:1},8,["to"])],64)):n("",!0),s("span",D," Page "+r(e.page)+" of "+r(e.last_page),1),e.page<e.last_page?(t(),a(_,{key:1},[l(p,{to:{name:"forms",query:{page:e.page+1,per_page:e.per_page}},class:"p-3 underline"},{default:d(()=>[c("Next ")]),_:1},8,["to"]),l(p,{to:{name:"forms",query:{page:e.last_page,per_page:e.per_page}},class:"p-3 underline"},{default:d(()=>[c("Last ")]),_:1},8,["to"])],64)):n("",!0)])]))])}const H=f(k,[["render",M],["__scopeId","data-v-149fff02"]]);export{H as default};
