// Convenience helpers
const $ = (sel) => document.querySelector(sel);
const msgBox = $("#msg");

function flash(text, type = "info") {
  msgBox.textContent = text;
  msgBox.className =
    "mb-4 p-3 rounded-lg " +
    (type === "error"
      ? "bg-red-100 text-red-700"
      : type === "success"
      ? "bg-green-100 text-green-700"
      : "bg-indigo-100 text-indigo-700");
  msgBox.hidden = false;
}

$("#ratio").addEventListener("input", (e) => {
  $("#ratioLabel").textContent = e.target.value;
});

$("#goBtn").addEventListener("click", async () => {
  const file = $("#fileInput").files[0];
  if (!file) {
    flash("Please choose an HTML file first", "error");
    return;
  }

  const opts = {
    stage0: $("#stage0").checked,
    stage1: $("#stage1").checked,
    stage2: $("#stage2").checked,
    mangle_ratio: parseFloat($("#ratio").value),
  };

  const formData = new FormData();
  formData.append("file", file);
  formData.append("options", JSON.stringify(opts));

  flash("Working… this may take a few seconds");

  try {
    const res = await fetch("/api/obfuscate", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error(await res.text());

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    const cd = res.headers.get("Content-Disposition") || "";
    const match = /filename\*=UTF-8''(.+)|filename="?([^\";]+)"?/.exec(cd);
    a.download = decodeURIComponent(match?.[1] || match?.[2] || "output.html");

    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    flash("File downloaded", "success");
  } catch (err) {
    console.error(err);
    flash("Error: " + err.message, "error");
  }
});