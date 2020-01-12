function addStaker(staker) {
    const markup = `
    <div class="cell" data-title="ID"><p>${staker.id}</p></div>
    <div class="cell name" data-title="Name">
      ${staker.logoUrl ? `
        <img class="float-left" src="${staker.logoUrl}">
      ` : `
        <i class="fas fa-question float-left icon"></i>
      `}
      <div class="float-left ml-3">
        <p class="text-left font-weight-bold"><span>${staker.name ? staker.name : "Unknown"}${staker.name && staker.keybasePubKey ? ` <i class="fas fa-check-circle verified"></i>` : ""}</span></p>
        <p class="text-left font-weight-light">${staker.address}</p>
      </div>
    </div>
    <div class="cell" data-title="Self-Staked"><p>${numeral(staker.selfStaked).format("0,0")} FTM</p></div>
    <div class="cell" data-title="Delegated"><p>${numeral(staker.delegated).format("0,0")} FTM</p></div>
    <div class="cell available" data-title="Available"><p>${numeral(staker.availableDelegationAmount).format("0,0")} FTM <span class="font-weight-light">(${numeral(staker.availableDelegationPercent).format("0.00%")})</span></p></div>
    <div class="cell contact" data-title="Contact">
    ${staker.contact ? `
      <a href="${staker.contact}" target="_blank">
        <i class="fas fa-globe-americas link"></i>
      </a>
    ` : ""}
    </div>
    `;

    const child = document.createElement("div");
    child.className = "row table-row";
    child.innerHTML = markup;

    document.querySelector(".table").appendChild(child);
}

(function ($) {
  axios.get("https://block42.uber.space:44220/api/v1/validators").then((response) => {
    response.data.forEach((staker) => {
      addStaker(staker);
    })
  })
})(jQuery);