import React from "react";

const Footer = () => {
  const logoSrc = '/images/projects/aclogo2.png';
  return (
    <footer className="footer border z-10 border-t-[#33353F] border-l-transparent border-r-transparent text-white">
      <div className="container p-12 flex justify-between">
        <span><img src={logoSrc} alt="Logo" className="h-auto w-20 md:w-40" /></span>
        <p className="text-slate-600">All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;