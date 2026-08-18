document.addEventListener("DOMContentLoaded", function () {

   const memberField = document.getElementById("id_member");
   const feeField = document.getElementById("id_fee_structure");
   const amountField = document.getElementById("id_amount_paid");

   if (!memberField || !feeField || !amountField) {
      return;
   }

   function updateRemainingBalance() {

      const outstanding = parseFloat(
         document
            .getElementById("outstanding")
            .textContent
            .replace("GH₵", "")
            .trim()
      ) || 0;

      const amount = parseFloat(amountField.value) || 0;

      let remaining = outstanding - amount;

      if (remaining < 0) {
         remaining = 0;
      }

      document.getElementById("remaining-after-payment").textContent =
         "GH₵ " + remaining.toFixed(2);
   }


   function loadBalance() {

      if (!memberField.value || !feeField.value) {
         return;
      }

      fetch(
         `/finance/payment-balance/?member=${memberField.value}&fee=${feeField.value}`
      )
         .then(response => response.json())

         .then(data => {

            document.getElementById("total-fee").textContent =
               "GH₵ " + data.total_fee;

            document.getElementById("total-paid").textContent =
               "GH₵ " + data.total_paid;

            document.getElementById("outstanding").textContent =
               "GH₵ " + data.outstanding;

            const statusElement = document.getElementById("payment-status");

            let badgeClass = "bg-secondary";

            if (data.status === "PAID") {
               badgeClass = "bg-success";
            } else if (data.status === "PARTIAL") {
               badgeClass = "bg-warning text-dark";
            } else if (data.status === "UNPAID") {
               badgeClass = "bg-danger";
            }

            statusElement.innerHTML = `
    <span class="badge ${badgeClass}">
        ${data.status}
    </span>`;

            updateRemainingBalance();

         })

         .catch(error => {
            console.error("Balance loading failed:", error);
         });

   }


   memberField.addEventListener("change", loadBalance);

   feeField.addEventListener("change", loadBalance);

   amountField.addEventListener("input", updateRemainingBalance);

});