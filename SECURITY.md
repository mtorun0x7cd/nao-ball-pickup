# Security Policy

## Status

This repository is an archived academic project (TH Köln, Special Aspects of
Mobile Autonomous Systems, Winter 2021/2022), retained for reference and
portfolio purposes. It is **not under active development** and receives no
functional or security updates.

## Not for production use

The code was written as a student exercise to drive a NAO robot on a lab
network, not as a hardened or deployable system. It controls the robot through
the NAOqi network protocol with no application-level authentication in this
configuration, and it expects a placeholder robot IP (`<robot-ip>`) rather than
any committed credential. It must not be operated outside a trusted, isolated lab
network.

## Known Limitations

The source carries the posture of student research code targeting Python 2.7 and
a legacy NAOqi Python SDK. These notes are recorded for transparency, not as a
maintenance backlog:

- **End-of-life toolchain.** The project requires Python 2.7 and a legacy NAOqi
  Python SDK, both unsupported and no longer receiving security fixes.
- **Unauthenticated robot link.** All image processing runs on a remote PC and
  exchanges camera frames and motor commands with the robot over the NAOqi
  network protocol with no application-level authentication; anyone able to reach
  the robot's control port on the network segment can drive it.
- **No input or failure handling.** Detection thresholds, head-tracking gains,
  and the pickup keyframes are hard-coded for a specific test setup; the robot
  has no balance feedback, so an out-of-distribution pose can cause it to fall.
- **No tests.** The repository ships no automated tests; correctness was assessed
  by observing the physical robot.

## Reporting

To report a substantive issue worth recording, contact info@mtorun0x7cd.com.
Given the archived status of the project, a fix or response is not guaranteed.
