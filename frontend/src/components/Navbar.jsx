import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Upload" },
  { to: "/history", label: "History" },
  { to: "/map", label: "Map" }
];

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand">RCM</div>
      <div className="nav-links">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            {item.label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

