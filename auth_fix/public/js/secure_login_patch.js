frappe.ready(() => {
  const originalCall = login.call;

  login.call = function (args, callback, url = '/') {
    if (args.pwd) {
      const secretKey = 'mysecurekey12345'; // must match backend
      const encrypted = encryptAES(args.pwd, secretKey);

      args.pwd = encrypted;
      args.cmd = 'auth_fix.auth_fix.api.secure_login';
    }

    return frappe.call({
      type: 'POST',
      url: url,
      args: args,
      callback: callback,
      freeze: true,
      statusCode: login.login_handlers,
    });
  };

  function encryptAES(plaintext, secret) {
    const key = CryptoJS.enc.Utf8.parse(secret);
    const encrypted = CryptoJS.AES.encrypt(plaintext, key, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7,
    });

    return encrypted.ciphertext.toString(CryptoJS.enc.Base64);
  }
});
