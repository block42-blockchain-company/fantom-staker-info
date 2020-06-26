function addValidator(validator) {
  const markup = `
  <div class="cell" data-title="ID"><p>${validator._id}</p></div>
  <div class="cell name" data-title="Name">
    ${validator.isCheater ? `
      <i class="fas fa-skull float-lg-left icon text-danger"></i>
    ` : `
      ${validator.isUnstaking ? `
        <i class="fas fa-exclamation-triangle float-lg-left icon text-warning"></i>
      ` : `
        ${validator.name ? `
          ${validator.logoUrl ? `<img class="float-lg-left" src="${validator.logoUrl}" alt="${validator.name} Logo">` : `<p class="float-lg-left icon"></p>`}
        ` : `
          <i class="fas fa-question float-lg-left icon"></i>
        `}
      `}
    `}
    <div class="float-lg-left ml-lg-3 mt-sm-2 mt-lg-0">
      <p class="text-lg-left ${validator.name ? "font-weight-bold" : ""} name"><span>${validator.name ? validator.name : "unknown"}${validator.name && validator.isVerified ? ` <i class="fas fa-check-circle verified" title="Verified via Blockchain"></i>` : ""}</span></p>
      <p class="text-lg-left font-weight-light text-truncate address"><a href="https://explorer.fantom.network/validator/${validator.address}" target="_blank">${validator.address.toLowerCase()}</a></p>
    </div>
  </div>
  <div class="cell" data-title="Self-Staked"><p>${numeral(validator.selfStakedAmount).format("0,0")} FTM</p></div>
  <div class="cell" data-title="Delegated"><p>${numeral(validator.delegatedAmount).format("0,0")} FTM</p></div>
  <div class="cell text-light" data-title="In Undelegation"><p>${numeral(validator.inUndelegationAmount).format("0,0")} FTM</p></div>
  <div class="cell" data-title="Total Staked"><p>${numeral(validator.totalStakedAmount).format("0,0")} FTM</p></div>
  <div class="cell" data-title="Available Capacity"><p>${numeral(validator.availableCapacityAmount).format("0,0")} FTM</p></div>
  <div class="cell text-light" data-title="Staking Power"><p>${numeral(validator.stakingPowerPercent).format("0.00%")}</p></div>
  <div class="cell links" data-title="Links">
  ${validator.website || validator.contact ? `
    ${validator.website ? `
      <a class="mr-1" href="${validator.website}" rel="nofollow" target="_blank">
        <i class="fas fa-globe-americas link"></i>
      </a>
    ` : ""}
    ${validator.contact ? `
      <a class="ml-1" href="${validator.contact}" rel="nofollow" target="_blank">
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
    child.className = `row entry ${validator.isCheater ? 'cheater' : validator.isUnstaking ? 'unstaking' : ''}`;
    child.title = `${validator.isCheater ? 'Cheater' : validator.isUnstaking ? 'Unstaking' : ''}`
    child.innerHTML = markup;

    document.querySelector(".table").appendChild(child);
}

function updateGeneral() {
  axios.get("https://fantomstaker.info/api/v1/general").then((response) => {
    const general = response.data;

    document.querySelector("#total-self-staked-sum").innerText = numeral(general.totalSelfStakedSum).format("0,0") + " FTM"
    document.querySelector("#total-self-staked-percent").innerText = numeral(general.totalSelfStakedPercent).format("0.00%")
    document.querySelector("#total-delegated-sum").innerText = numeral(general.totalDelegatedSum).format("0,0") + " FTM"
    document.querySelector("#total-delegated-percent").innerText = numeral(general.totalDelegatedPercent).format("0.00%")
    document.querySelector("#total-in-undelegation-sum").innerText = numeral(general.totalInUndelegationSum).format("0,0") + " FTM"
    document.querySelector("#total-in-undelegation-percent").innerText = numeral(general.totalInUndelegationPercent).format("0.00%")
    document.querySelector("#total-staked-sum").innerText = numeral(general.totalStakedSum).format("0,0") + " FTM"
    document.querySelector("#total-staked-percent").innerText = numeral(general.totalStakedPercent).format("0.00%")
    
    // Total staked progress
    const totalStakedPercent = numeral(general.totalStakedPercent).format("0.00%")
    const totalStakedProgressBar = document.querySelector(".progress-bar-total-staked")
    totalStakedProgressBar.innerText = totalStakedPercent
    totalStakedProgressBar.setAttribute("style", `width: ${totalStakedPercent}`)
    totalStakedProgressBar.setAttribute("aria-valuenow", totalStakedPercent.replace("%", ""))

    // Total supply
    document.querySelector("#total-supply").innerText = numeral(general.totalSupply).format("0,0")

    // Reward unlock
    const rewardUnlockDate = new Date()
    rewardUnlockDate.setTime(general.rewardUnlockDate * 1000)
    document.querySelector("#reward-roi").innerText = numeral(general.roi).format("0.00%")
    document.querySelector("#reward-validator-roi").innerText = numeral(general.validatorRoi).format("0.00%")

    // Last updated
    const lastUpdated = new Date()
    lastUpdated.setTime(general.lastUpdated * 1000)
    document.querySelector("#last-updated").innerText = lastUpdated.toLocaleString([], { dateStyle: "short", timeStyle: "short" })
  })
}

function updateValidators() {
  const hideUnknown = window.localStorage.getItem("hideUnknown");
  const sortBy = JSON.parse(window.localStorage.getItem("sortBy"));

  // Fetch validators from backend
  axios.get("https://fantomstaker.info/api/v1/validators?hideUnknown=" + hideUnknown + "&sortKey=" + sortBy.sortKey + "&order=" + sortBy.order).then((response) => {
    const validators = response.data;

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

function sort() {
  const element = event.srcElement;
  const sortKey = element.getAttribute("sort-key");

  // Get previous sort
  const sortBy = JSON.parse(window.localStorage.getItem("sortBy"));
  const previousSortKey = sortBy.sortKey;
  const previousOrder = sortBy.order;
  
  // Change/Toggle sort order and update sort key
  sortBy.order = (previousSortKey == sortKey && previousOrder == 'desc') ? 'asc' : 'desc';
  sortBy.sortKey = sortKey;

  // Update local storage
  window.localStorage.setItem("sortBy", JSON.stringify(sortBy));

  // Remove sort indicator from previous element
  document.querySelector("div .row.header .cell svg").parentElement.innerHTML = ""

  // Apply sort indicator to current element
  element.querySelector("span").innerHTML = `<i class='fas fa-sort-${sortBy.order == 'desc' ? 'down' : 'up'}'></i>`

  // Update data
  updateValidators();
}

(function ($) {
  let hideUnknown = window.localStorage.getItem("hideUnknown");
  let sortBy = JSON.parse(window.localStorage.getItem("sortBy"));

  // Update local storage
  if (hideUnknown === null) {
    hideUnknown = "true";
    window.localStorage.setItem("hideUnknown", hideUnknown);
  }

  // Update local storage
  if (sortBy === null) {
    sortBy = { sortKey: '_id', order: 'asc' };
    window.localStorage.setItem("sortBy", JSON.stringify(sortBy));
  }

  // TODO @C: Temporary migration, remove in the future
  if (sortBy != null && sortBy.sortKey == 'id') {
    sortBy = { sortKey: '_id', order: 'asc' };
    window.localStorage.setItem("sortBy", JSON.stringify(sortBy));
  }

  // Update switch state
  document.querySelector("#hideUnknown").checked = hideUnknown == "true";

  // Update sort indicator
  document.querySelector(`div .row.header .cell [sort-key='${sortBy.sortKey}'] span`).innerHTML = `<i class='fas fa-sort-${sortBy.order == 'desc' ? 'down' : 'up'}'></i>`

  // Update data
  updateGeneral();
  updateValidators();
})();