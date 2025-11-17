const STORAGE_KEY = "silicium_data_v1";
const sound = document.getElementById("notif-sound");

function loadData(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { projects: [] } }
  catch(e){ return { projects: [] } }
}
function saveData(data){ localStorage.setItem(STORAGE_KEY, JSON.stringify(data)) }

let state = loadData();
let currentProjectId = null;

/* UTIL */
function uid(){ return Date.now().toString(36) + Math.random().toString(36).slice(2,8) }

/* --- Modal utilities (in-site prompt/confirm/alert) --- */
const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const modalActions = document.getElementById("modal-actions");

function showModal({title = "", body = "", placeholder = "", input = false, buttons = [{id:"ok", label:"OK", cls:"btn-primary"}]}) {
  return new Promise(resolve => {
    modalTitle.textContent = title;
    modalBody.innerHTML = "";
    if(input){
      const ta = document.createElement("textarea");
      ta.value = body || "";
      ta.placeholder = placeholder || "";
      ta.style.width = "100%";
      ta.style.minHeight = "80px";
      ta.style.borderRadius = "8px";
      ta.style.padding = "8px";
      ta.style.background = "rgba(255,255,255,0.02)";
      ta.style.color = "#fff";
      modalBody.appendChild(ta);
      ta.focus();
    } else {
      const p = document.createElement("div"); p.innerHTML = body; modalBody.appendChild(p);
    }
    modalActions.innerHTML = "";
    buttons.forEach(b=>{
      const btn = document.createElement("button");
      btn.textContent = b.label;
      btn.className = b.cls || "btn-ghost";
      btn.onclick = ()=> {
        const val = input ? modalBody.querySelector("textarea").value : null;
        hideModal();
        resolve({id: b.id, value: val});
      };
      modalActions.appendChild(btn);
    });
    modal.classList.remove("hidden");
  });
}
function hideModal(){ modal.classList.add("hidden"); modalBody.innerHTML = ""; modalActions.innerHTML = ""; }

/* RENDER */
function renderProjects(){
  const ul = document.getElementById("projects-list"); ul.innerHTML = "";
  state.projects.forEach(p=>{
    const li = document.createElement("li");
    li.textContent = p.name;
    li.dataset.id = p.id;
    li.onclick = ()=>selectProject(p.id);
    if(p.id === currentProjectId) li.classList.add("active");
    ul.appendChild(li);
  });
}
function renderChats(){
  const ul = document.getElementById("chats-list"); ul.innerHTML = "";
  if(!currentProjectId) return;
  const proj = state.projects.find(p=>p.id===currentProjectId);
  if(!proj) return;
  (proj.conversations || []).forEach(conv=>{
    const li = document.createElement("li");
    li.textContent = conv.title || ("Chat • " + new Date(conv.created).toLocaleString());
    li.onclick = ()=>openConversation(conv.id);
    ul.appendChild(li);
  });
}
function renderMessages(conversation){
  const container = document.getElementById("messages"); container.innerHTML = "";
  if(!conversation) return;
  conversation.messages.forEach((m, idx)=>{
    const div = document.createElement("div");
    div.className = "msg " + (m.role==="user" ? "user" : "assistant");
    if(m.stale) div.classList.add("stale");
    const content = document.createElement("div");
    content.textContent = m.content;
    div.appendChild(content);

    const meta = document.createElement("div"); meta.className = "msg-meta";
    if(m.role === "user"){
      const editBtn = document.createElement("button");
      editBtn.className = "edit-btn";
      editBtn.textContent = "Modifier";
      editBtn.onclick = ()=> beginEditMessage(conversation, m.id);
      meta.appendChild(editBtn);
    } else {
      // assistant: add regenerate button if stale or always available
      const regen = document.createElement("button");
      regen.className = "regen-btn";
      regen.textContent = "Régénérer";
      regen.onclick = ()=> regenerateAssistant(conversation, idx);
      meta.appendChild(regen);
      if(m.stale){
        const note = document.createElement("span"); note.textContent = "Réponse obsolète";
        note.style.color = "var(--muted)"; note.style.fontSize = "12px";
        meta.appendChild(note);
      }
    }
    div.appendChild(meta);
    container.appendChild(div);
  });
  container.scrollTop = container.scrollHeight;
  document.getElementById("project-title").textContent = getProjectName(currentProjectId);
}

/* ACTIONS */
function getProjectName(id){ const p = state.projects.find(x=>x.id===id); return p ? p.name : "Welcome" }

async function createProject(){
  const res = await showModal({
    title: "Créer un projet",
    body: "",
    input: true,
    placeholder: "Nom du projet",
    buttons: [{id:"cancel", label:"Annuler", cls:"btn-ghost"},{id:"create", label:"Créer", cls:"btn-primary"}]
  });
  if(res.id !== "create" || !res.value) return;
  const name = res.value.trim();
  if(!name) return;
  const newP = { id: uid(), name, conversations: [] };
  state.projects.unshift(newP);
  saveData(state);
  currentProjectId = newP.id;
  renderAll();
}

async function deleteProject(){
  if(!currentProjectId) return;
  const res = await showModal({
    title: "Supprimer le projet",
    body: "Supprimer le projet et ses conversations ?",
    buttons: [{id:"no", label:"Non", cls:"btn-ghost"},{id:"yes", label:"Oui, supprimer", cls:"btn-primary"}]
  });
  if(res.id !== "yes") return;
  state.projects = state.projects.filter(p=>p.id!==currentProjectId);
  currentProjectId = state.projects.length ? state.projects[0].id : null;
  saveData(state);
  renderAll();
}

function newConversation(initialPrompt){
  if(!currentProjectId) return alertInSite("Sélectionne un projet d'abord");
  const proj = state.projects.find(p=>p.id===currentProjectId);
  const conv = { id: uid(), title: initialPrompt?.slice(0,40), created: Date.now(), messages: [] };
  proj.conversations.unshift(conv);
  saveData(state);
  renderChats();
  openConversation(conv.id);
  return conv;
}

function openConversation(convId){
  const proj = state.projects.find(p=>p.id===currentProjectId);
  if(!proj) return;
  const conv = proj.conversations.find(c=>c.id===convId);
  if(!conv) return;
  renderMessages(conv);
  document.getElementById("composer").dataset.conv = conv.id;
  updateComposerState(conv);
}

/* composer editing workflow */
function beginEditMessage(conversation, messageId){
  const conv = conversation;
  const msg = conv.messages.find(m=>m.id===messageId);
  if(!msg) return;
  const ta = document.getElementById("prompt");
  ta.value = msg.content;
  ta.focus();
  document.getElementById("send-btn").textContent = "Mettre à jour";
  document.getElementById("composer").dataset.editing = messageId;
}

function updateComposerState(conv){
  const composer = document.getElementById("composer");
  const ta = document.getElementById("prompt");
  // center composer if conversation empty
  if(conv.messages.length === 0){
    composer.classList.add("centered");
    ta.placeholder = "Démarre la conversation... Tape un prompt et appuie Envoyer";
  } else {
    composer.classList.remove("centered");
    ta.placeholder = "Écris ton prompt ici...";
  }
  // reset editing UI
  if(!composer.dataset.editing) document.getElementById("send-btn").textContent = "Envoyer";
}

/* send / update logic */
// ...existing code...

async function sendPrompt(){
  const ta = document.getElementById("prompt");
  const prompt = ta.value.trim();
  if(!prompt) return;
  if(!currentProjectId) { alertInSite("Crée un projet d'abord"); return }

  const proj = state.projects.find(p=>p.id===currentProjectId);
  let conv = proj.conversations[0];
  if(!conv) conv = newConversation(prompt);

  const composer = document.getElementById("composer");
  const editingId = composer.dataset.editing;
  if(editingId){
    // update existing user message
    const msgIndex = conv.messages.findIndex(m=>m.id===editingId);
    if(msgIndex === -1) return;
    conv.messages[msgIndex].content = prompt;
    // mark assistant messages after this user message as stale
    for(let i = msgIndex + 1; i < conv.messages.length; i++){
      if(conv.messages[i].role === "assistant") conv.messages[i].stale = true;
    }
    delete composer.dataset.editing;
    document.getElementById("send-btn").textContent = "Envoyer";
    saveData(state);
    renderMessages(conv);
    // ensure composer goes to bottom after edit
    updateComposerState(conv);
    ta.value = ""; ta.focus();
    return;
  }


 // normal send
  if(!conv) return;
  const userMsg = { id: uid(), role:"user", content: prompt, time: Date.now() };
  conv.messages.push(userMsg);
  saveData(state);
  renderMessages(conv);

  // after first user message, update composer state (remove centered)
  updateComposerState(conv);

  ta.value = ""; ta.focus();

  const assistantText = await generateResponse(prompt, conv);
  const assistantMsg = { id: uid(), role:"assistant", content: assistantText, time: Date.now(), stale:false };
  conv.messages.push(assistantMsg);
  saveData(state);
  renderMessages(conv);
  try{ sound && sound.play().catch(()=>{}) }catch(e){}
}

/* regenerate assistant message */
async function regenerateAssistant(conv, assistantIndex){
  // find the preceding user prompt to use as seed
  // find previous user message before assistantIndex
  let seed = "";
  for(let i = assistantIndex -1; i >=0; i--){
    if(conv.messages[i].role === "user"){ seed = conv.messages[i].content; break; }
  }
  if(!seed) return alertInSite("Impossible de trouver le prompt associé.");
  const newText = await generateResponse(seed, conv);
  conv.messages[assistantIndex].content = newText;
  conv.messages[assistantIndex].stale = false;
  saveData(state);
  renderMessages(conv);
}

/* SIMULATED AI -- replace with real API call */
function sleep(ms){ return new Promise(r=>setTimeout(r,ms)) }
async function generateResponse(prompt, conv){
  await sleep(600 + Math.random()*800);
  const reply = `Réponse Silicium → ${prompt.split("").reverse().join("").slice(0,240)}…`;
  return reply;
}

/* IMPORT/EXPORT */
function exportData(){
  const blob = new Blob([JSON.stringify(state, null, 2)], {type:"application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "silicium_backup.json";
  a.click();
}
function importData(){
  const inp = document.createElement("input");
  inp.type = "file"; inp.accept = "application/json";
  inp.onchange = e=>{
    const f = e.target.files[0];
    if(!f) return;
    const reader = new FileReader();
    reader.onload = ev=>{
      try{
        const data = JSON.parse(ev.target.result);
        state = data;
        saveData(state);
        currentProjectId = state.projects?.[0]?.id || null;
        renderAll();
        showModal({title:"Import", body:"Import OK", buttons:[{id:"ok",label:"OK",cls:"btn-primary"}]});
      }catch(err){ showModal({title:"Erreur", body:"Fichier invalide", buttons:[{id:"ok",label:"OK",cls:"btn-primary"}]}) }
    };
    reader.readAsText(f);
  };
  inp.click();
}

/* small in-site alert helper */
function alertInSite(message){
  showModal({title:"Info", body: message, buttons:[{id:"ok", label:"OK", cls:"btn-primary"}]});
}

/* UI wiring */
function selectProject(id){
  currentProjectId = id;
  renderAll();
  const proj = state.projects.find(p=>p.id===id);
  if(proj?.conversations?.length) openConversation(proj.conversations[0].id);
}
function renderAll(){
  renderProjects(); renderChats();
  if(currentProjectId){
    const proj = state.projects.find(p=>p.id===currentProjectId);
    if(proj && proj.conversations && proj.conversations.length) openConversation(proj.conversations[0].id);
    else { document.getElementById("messages").innerHTML = `<div class="msg assistant">Projet vide. Tape un prompt pour commencer.</div>`; updateComposerState({messages:[]}); }
  } else {
    document.getElementById("messages").innerHTML = `<div class="msg assistant">Crée ou sélectionne un projet pour démarrer.</div>`; updateComposerState({messages:[]});
  }
}

/* Init */
document.getElementById("new-project-btn").onclick = createProject;
document.getElementById("delete-project").onclick = deleteProject;
document.getElementById("send-btn").onclick = sendPrompt;
document.getElementById("clear-btn").onclick = ()=>{ document.getElementById("prompt").value = "" }
document.getElementById("export-btn").onclick = exportData;
document.getElementById("import-btn").onclick = importData;
document.getElementById("composer").onsubmit = e=>{ e.preventDefault(); sendPrompt(); }
modal.onclick = (e)=> { if(e.target === modal) hideModal(); }

if(state.projects.length === 0){
  const demo = { id: uid(), name: "Demo", conversations: [] };
  state.projects.push(demo);
  currentProjectId = demo.id;
  saveData(state);
} else {
  currentProjectId = state.projects[0].id;
}
renderAll();