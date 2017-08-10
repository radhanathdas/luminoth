import numpy as np
import tensorflow as tf

from luminoth.utils.anchors import generate_anchors_reference, generate_anchors_reference_old


class AnchorsTest(tf.test.TestCase):

    def _get_widths_heights(self, anchor_reference):
        return np.column_stack((
            (anchor_reference[:, 2] - anchor_reference[:, 0] + 1),
            (anchor_reference[:, 3] - anchor_reference[:, 1] + 1)
        ))

    def testAnchorReference(self):
        # Test simple case with one aspect ratio and one scale.
        base_size = 256
        aspect_ratios = [1.]
        scales = [1.]
        anchor_reference = generate_anchors_reference(
            base_size=base_size,
            aspect_ratios=aspect_ratios,
            scales=scales
        )

        # Should return a single anchor.
        self.assertEqual(anchor_reference.shape, (1, 4))
        self.assertAllEqual(
            anchor_reference[0], [0, 0, base_size - 1, base_size - 1]
        )

        # Test with fixed ratio and different scales.
        scales = np.array([0.5, 1., 2., 4.])
        anchor_reference = generate_anchors_reference(
            base_size=base_size,
            aspect_ratios=aspect_ratios,
            scales=scales
        )

        # Check that we have the correct number of anchors.
        self.assertEqual(anchor_reference.shape, (4, 4))
        width_heights = self._get_widths_heights(anchor_reference)
        # Check that anchors are squares (aspect_ratio = [1.0]).
        self.assertTrue((width_heights[:, 0] == width_heights[:, 1]).all())
        # Check that widths are consistent with scales times base_size.
        self.assertAllEqual(width_heights[:, 0], base_size * scales)
        # Check exact values.
        self.assertAllEqual(
            anchor_reference,
            np.array([[64., 64., 191., 191.],
                      [0., 0., 255., 255.],
                      [-128., -128., 383., 383.],
                      [-384., -384., 639., 639.]])
        )

        # Test with different ratios and scales.
        scales = np.array([0.5, 1., 2.])
        aspect_ratios = np.array([0.5, 1., 2.])
        anchor_reference = generate_anchors_reference(
            base_size=base_size,
            aspect_ratios=aspect_ratios,
            scales=scales
        )

        # Check we have the correct number of anchors.
        self.assertEqual(
            anchor_reference.shape, (len(scales) * len(aspect_ratios), 4)
        )

        width_heights = self._get_widths_heights(anchor_reference)

        # Check ratios of height / widths
        anchor_ratios = width_heights[:, 1] / width_heights[:, 0]
        # Check scales (applied to )
        anchor_scales = np.sqrt(
            (width_heights[:, 1] * width_heights[:, 0]) / (base_size ** 2)
        )

        # Test that all ratios are used in the correct order.
        self.assertAllClose(
            anchor_ratios, [0.5, 0.5, 0.5, 1., 1., 1., 2., 2., 2.]
        )
        # Test that all scales are used in the correct order.
        self.assertAllClose(
            anchor_scales, [0.5, 1., 2., 0.5, 1., 2., 0.5, 1., 2.]
        )


if __name__ == '__main__':
    tf.test.main()
