# 20MG release controller distribution

Enrollment-only owner preparation packet. Controller source remains in a separate private repository. This repo is never deployed with the portal.

Download `owner-preparation.zip`, unzip it on your owner device, then open `owner-steps.html` and `owner-packet.html` locally. The latter fills only your approval hostname, SSH public key and owner CIDR; it generates the cloud-init file without sending those values anywhere. Never enter a private key, token or enrollment ticket.

## Fixed download

Versioned release: https://github.com/kylelgm/20mg-release-controller-dist/releases/tag/enrollment-5e13b7a

Public capsule SHA256: `de3640b29e7a529720db777563da8d71add362b2fcbf039ddbc8aa6fb07784eb`.

Cloud-init also downloads CLI 2.40.0 directly from 1Password's official HTTPS distribution and checks SHA256 `74277219e8da60958c00f9aee9d2023225e98fdda8bfd2156a5d9e85e0edaab3`. This public repo does not redistribute the proprietary CLI. The helper restores the exact original bundle and checks SHA256 `c99e36c06609f8157fb9a360ae4ec19e0f09aef836518c920e8705fb35c17eaa` before extracting or installing anything. Both download digests are pinned in the owner packet. No GitHub access token or production credential is needed. Failed downloads, changed bytes or compression differences stop installation.

Reviewed source commit: `5e13b7a94b359678829d611610607a7d795c53ea`; supported target: fresh Ubuntu 24.04 x86-64 only. No self-update or overwrite.

## Locks and policy

Production credential import, candidate submission and all provider execution are permanently disabled in this build. Passkey enrollment is enabled. The enrollment policy digest is SHA256 of the exact bytes of `enrollment-policy.json`: `5bbd47b467e880442ab4168199e65c9d3a115ff9a8776b58d10cb49dce1dd422`. It is not a production release policy. `submitterHash` is the SHA256 of a discarded random 32-byte preimage; no usable submitter token exists. Future reviewed owner maintenance must supply a new policy and submission credential; this packet cannot activate production.

## Publication inspection

Archive inventory: 2297 regular files, zero links; all 1135 text files scanned for credential markers, local home paths, private keys and domains. No production credentials or internal 20MG hostnames found. Vendor binaries contain generic parser strings such as OPENSSH PRIVATE KEY and metadata.google.internal; those are vendor code strings, not embedded keys or 20MG infrastructure. Public API/vendor/doc URLs and npm author attribution remain. Bundle metadata exposes the private controller repo name, source commit and fixed portal repository name; no private repository contents beyond the distributed compiled controller/installer, hostname, provider account IDs, client data, environment files or production config are included. Node and Caddy notices are in `licenses/`; npm notices remain in the capsule.

1Password CLI is fetched by the owner machine rather than republished, consistent with its [Developer Tools terms](https://1password.com/legal/api-sdk-terms-of-service).

## Evidence limits

Earlier native Ubuntu synthetic installer rehearsal covered this exact original bundle. This packet adds tokenless distribution and exact reconstitution. Real Hetzner/TLS, iPhone Face ID, vault isolation and actual agent denial remain owner-boundary acceptance work. No production credentials have been handled.
