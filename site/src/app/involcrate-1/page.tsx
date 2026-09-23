export default function InvolcrateOneRedirectPage() {
  return (
    <>
      <meta httpEquiv="refresh" content="0; url=/vision" />
      <p style={{ padding: "4rem", textAlign: "center" }}>
        Redirigiendo a <a href="/vision">/vision</a>…
      </p>
    </>
  );
}
