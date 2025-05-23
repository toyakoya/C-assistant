export async function OnlineSolve(model, inf) {
  const res = await fetch("http://127.0.0.1:8000/chat/onlinesolve/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model: model, inf: inf }),
  });
  const data = await res.json();
  console.log(data);
  return data;
}
