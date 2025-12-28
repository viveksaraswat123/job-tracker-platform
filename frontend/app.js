let jobs = JSON.parse(localStorage.getItem("jobs")) || [];
updateStats();
renderTable();

function updateStats(){
  document.getElementById("total-users").innerText = 1;
  document.getElementById("total-apps").innerText = jobs.length;
  document.getElementById("offers").innerText = jobs.filter(j=>j.status==="Offer").length;
}

function renderTable(list = jobs){
  const tbody = document.getElementById("app-list");
  tbody.innerHTML = "";

  list.forEach((job, index)=>{
    const badge = getBadge(job.status);
    tbody.innerHTML += `
    <tr class="border-b">
      <td class="py-2">${job.company}</td>
      <td>${job.role}</td>
      <td>${badge}</td>
      <td>${job.date}</td>
      <td class="space-x-2">
        <button onclick="editJob(${index})" class="border px-2 py-1 rounded">Edit</button>
        <button onclick="deleteJob(${index})" class="border px-2 py-1 rounded">Del</button>
      </td>
    </tr>`;
  });

  updateStats();
}

function getBadge(status){
  const map = {
    "Applied": "bg-blue-100 text-blue-700",
    "Interview": "bg-yellow-100 text-yellow-700",
    "Rejected": "bg-red-100 text-red-700",
    "Offer": "bg-green-100 text-green-700"
  };
  return `<span class="px-2 py-1 rounded-full text-sm ${map[status]}">${status}</span>`;
}

function addJob(){
  const company = document.getElementById("company").value.trim();
  const role = document.getElementById("role").value.trim();
  const status = document.getElementById("status").value;
  const date = document.getElementById("date").value;

  if(!company || !role || !date){
    alert("Fill all fields BKL");
    return;
  }

  jobs.push({company, role, status, date});
  localStorage.setItem("jobs", JSON.stringify(jobs));
  closeModal();
  renderTable();
}

function deleteJob(i){
  jobs.splice(i,1);
  localStorage.setItem("jobs", JSON.stringify(jobs));
  renderTable();
}

function editJob(i){
  const job = jobs[i];
  document.getElementById("company").value = job.company;
  document.getElementById("role").value = job.role;
  document.getElementById("status").value = job.status;
  document.getElementById("date").value = job.date;
  openModal();
  jobs.splice(i,1);
}

function searchTable(){
  const q = document.getElementById("search").value.toLowerCase();
  const f = jobs.filter(j=>j.company.toLowerCase().includes(q));
  renderTable(f);
}

function filterStatus(){
  const v = document.getElementById("filter").value;
  if(v==="ALL") renderTable();
  else renderTable(jobs.filter(j=>j.status===v));
}

function openModal(){ document.getElementById("modal").classList.remove("hidden"); }
function closeModal(){ 
  document.getElementById("modal").classList.add("hidden");
  ["company","role","date"].forEach(id=>document.getElementById(id).value="");
}
function toggleTheme(){
  const b = document.getElementById("body");
  b.classList.toggle("bg-gray-900");
  b.classList.toggle("text-white");
}
