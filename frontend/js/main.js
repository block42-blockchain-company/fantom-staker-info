function addStaker(staker) {
    const markup = `
    <div class="cell" data-title="ID"><p>${staker.id}</p></div>
    <div class="cell name" data-title="Name">
      ${staker.logoUrl ? `
        <img class="float-lg-left" src="${staker.logoUrl}">
      ` : `
        <i class="fas fa-question float-lg-left icon"></i>
      `}
      <div class="float-lg-left ml-lg-3 mt-sm-2 mt-lg-0">
        <p class="text-lg-left font-weight-bold name"><span>${staker.name ? staker.name : "Unknown"}${staker.name && staker.keybasePubKey ? ` <i class="fas fa-check-circle verified"></i>` : ""}</span></p>
        <p class="text-lg-left font-weight-light address">${staker.address.toLowerCase()}</p>
      </div>
    </div>
    <div class="cell" data-title="Self-Staked"><p>${numeral(staker.selfStaked).format("0,0")} FTM</p></div>
    <div class="cell" data-title="Total Staked"><p>${numeral(staker.totalStaked).format("0,0")} FTM</p></div>
    <div class="cell available" data-title="Available"><p>${numeral(staker.availableDelegationAmount).format("0,0")} FTM</p></div>
    <div class="cell contact" data-title="Links">
    ${staker.website ? `
      <a class="mr-1" href="${staker.website}" target="_blank">
        <i class="fas fa-globe-americas link"></i>
      </a>
    ` : ""}
    ${staker.contact ? `
      <a class="ml-1" href="${staker.contact}" target="_blank">
        <i class="fas fa-headset link"></i>
      </a>
    ` : ""}
    </div>
    `;

    const child = document.createElement("div");
    child.className = "row entry";
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