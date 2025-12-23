export async function request(url, options = {}) {
  const res = await fetch(`http://localhost:5000/api${url}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (res.status === 401) {
    window.location.href = "/staff/login";
    return;
  }

  return res.json();
}
