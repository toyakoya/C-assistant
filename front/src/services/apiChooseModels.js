export async function getModels() {
  const res = await fetch("http://127.0.0.1:8000/chat/models/", {
    method: "GET",
  });
  const data = await res.json();
  return data.models;
}
