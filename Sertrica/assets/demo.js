document.getElementById("encryptBtn").addEventListener("click", () => process("encrypt"));
document.getElementById("decryptBtn").addEventListener("click", () => process("decrypt"));

async function process(action) {
  const input = document.getElementById("input").value;
  const encType = document.getElementById("encType").value;
  const output = document.getElementById("output");
  const spinner = document.getElementById("spinner");

  if (!input.trim()) {
    output.value = "Error: Please enter some text.";
    return;
  }

  spinner.style.display = "flex"; // Ensure spinner is visible
  output.value = "";

  setTimeout(() => {
    try {
      let result;
      if (encType === "aes") {
        result = action === "encrypt" ? aesEncrypt(input) : aesDecrypt(input);
      } else if (encType === "aes_rsa") {
        result = action === "encrypt" ? aesRsaEncrypt(input) : aesRsaDecrypt(input);
      } else {
        throw new Error("Unsupported encryption type. Please select a valid option.");
      }
      output.value = result;
    } catch (error) {
      output.value = `Error: ${error.message}`;
    } finally {
      spinner.style.display = "none";
    }
  }, 500); // Simulate processing delay
}

function aesEncrypt(text) {
  // Simulated AES encryption (replace with real implementation)
  return btoa(text); // Base64 as a placeholder
}

function aesDecrypt(text) {
  // Simulated AES decryption (replace with real implementation)
  try {
    return atob(text); // Base64 as a placeholder
  } catch {
    throw new Error("Invalid AES encrypted text.");
  }
}

function aesRsaEncrypt(text) {
  // Simulated AES+RSA hybrid encryption (replace with real implementation)
  return `AES+RSA(${btoa(text)})`; // Placeholder
}

function aesRsaDecrypt(text) {
  // Simulated AES+RSA hybrid decryption (replace with real implementation)
  if (text.startsWith("AES+RSA(") && text.endsWith(")")) {
    try {
      return atob(text.slice(8, -1)); // Placeholder
    } catch {
      throw new Error("Invalid AES+RSA encrypted text.");
    }
  }
  throw new Error("Invalid AES+RSA encrypted text.");
}