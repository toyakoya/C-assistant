export async function GetProblem(url, cookies) {
  const res = await fetch("http://127.0.0.1:8000/chat/getproblem/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: url,
      cookies: cookies,
    }),
  });
  const data = await res.json();
  console.log(data);
  return data;
}
