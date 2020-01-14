function addValidator(validator) {
    const markup = `
    <div class="cell" data-title="ID"><p>${validator.id}</p></div>
    <div class="cell name" data-title="Name">
      ${validator.isCheater ? `
        <i class="fas fa-skull float-lg-left icon text-danger"></i>
      ` : `
        ${validator.name ? `
          ${validator.logoUrl ? `<img class="float-lg-left" src="${validator.logoUrl}">` : `<p class="float-lg-left icon"></p>`}
        ` : `
          <i class="fas fa-question float-lg-left icon"></i>
        `}
      `
      }
      <div class="float-lg-left ml-lg-3 mt-sm-2 mt-lg-0">
        <p class="text-lg-left ${validator.name ? "font-weight-bold" : ""} name"><span>${validator.name ? validator.name : "unknown"}${validator.name && validator.isVerified ? ` <i class="fas fa-check-circle verified" title="Verified via Blockchain"></i>` : ""}</span></p>
        <p class="text-lg-left font-weight-light address"><a href="https://explorer.fantom.network/validator/${validator.id}">${validator.address.toLowerCase()}</a></p>
      </div>
    </div>
    <div class="cell" data-title="Self-Staked"><p>${numeral(validator.selfStaked).format("0,0")} FTM</p></div>
    <div class="cell" data-title="Total Staked"><p>${numeral(validator.totalStaked).format("0,0")} FTM</p></div>
    <div class="cell available" data-title="Available"><p>${numeral(validator.availableDelegationAmount).format("0,0")} FTM</p></div>
    <div class="cell" data-title="Productivity"><p>${numeral(validator.productivity).format("0.00%")}</p></div>
    <div class="cell links" data-title="Links">
    ${validator.website || validator.contact ? `
      ${validator.website ? `
        <a class="mr-1" href="${validator.website}" target="_blank">
          <i class="fas fa-globe-americas link"></i>
        </a>
      ` : ""}
      ${validator.contact ? `
        <a class="ml-1" href="${validator.contact}" target="_blank">
          <i class="fas fa-headset link"></i>
        </a>
      ` : ""}
    ` : `
      <p>-</p>
    `
    }
    </div>
    `;

    const child = document.createElement("div");
    child.className = "row entry";
    child.innerHTML = markup;

    document.querySelector(".table").appendChild(child);
}

function updateValidators() {
  const hideUnknown = window.localStorage.getItem("hideUnknown");

  // Fetch validators from backend
  axios.get("https://fantomstaker.info:44220/api/v1/validators").then((response) => {
    let validators = response.data;

    if (hideUnknown == "true") {
      validators = validators.filter((validator) => validator.name)
    }

    // Get all table rows 
    const tableRows = document.querySelector(".table").children;
    const tableRowCount = tableRows.length;

    // Remove all table rows except the header row
    for (i = 1; i < tableRowCount; i++) {
      tableRows[1].remove();
    }

    // Add validator to the table
    validators.forEach((validator) => { addValidator(validator); })
  })
}

(function ($) {
  let hideUnknown = window.localStorage.getItem("hideUnknown");

  if (hideUnknown === null) {
    window.localStorage.setItem("hideUnknown", "false");
    hideUnknown = "false";
  }

  // Update switch state
  document.querySelector("#hideUnknown").checked = hideUnknown == "true";

  // Update validators
  updateValidators();
})();