export const sendFormData = async (data) => {
  try {
    const sendData = {
      username: data.userName,
      year: parseInt(data.year),
      month: parseInt(data.month),
      hours: parseInt(data.numberOfHours),
      project_name: data.projectName,
      task: data.tasks.split(","),
    };

    return await fetch("https://049945.xyz/api/file", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendData),
    }).then((response) => {
      const filename = response.headers
        .get("content-disposition")
        .split("filename=")[1]
        .replaceAll('"', "")
        .replaceAll("*=UTF-8", "");
      response.blob().then((blob) => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = decodeURI(filename);
        a.click();
      });
    });
  } catch (error) {
    throw new Error("Network error: " + error.message);
  }
};
