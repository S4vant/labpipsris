const items = [{ label: "Продукты", link: "/products" }];

export function Sidebar() {
  return (
    <div>
      {items.map(({ label, link }) => (
        <a href={link}>{label}</a>
      ))}
    </div>
  );
}
